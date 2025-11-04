"""
Core save file management operations for Space Chef
"""
import json
import re
import zipfile
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict
from models import SaveFile, Backup


class SaveManager:
    """Manages Space Chef save files and backups"""

    def __init__(self, save_path: Path):
        self.save_path = Path(save_path)
        self.backup_path = self.save_path / "Backup"
        self._player_name_cache: Dict[int, str] = {}  # Cache player names by slot

    def scan_saves(self) -> List[SaveFile]:
        """
        Scan the Saves folder for all save files and extract player information
        Returns a list of SaveFile objects sorted by slot number
        """
        saves = []

        if not self.save_path.exists():
            return saves

        # Look for save files (both .zip and .json patterns)
        # Pattern: save0008.json, save0100_day_30.zip, etc.
        for file_path in self.save_path.iterdir():
            if file_path.is_file() and file_path.name.startswith('save'):
                # Extract slot number from filename
                match = re.match(r'save(\d+)', file_path.name)
                if match:
                    slot = int(match.group(1))

                    # Get player name (use cache if available)
                    player_name = self._get_player_name(slot)

                    # Extract day from filename if present, otherwise try to read from JSON
                    day_match = re.search(r'day[_\s](\d+)', file_path.name, re.IGNORECASE)
                    if day_match:
                        day = int(day_match.group(1))
                    else:
                        # Try to get day from JSON file
                        day = self._get_day_from_json(slot)
                        if day is None:
                            day = 0

                    # Get last modified time
                    last_modified = datetime.fromtimestamp(file_path.stat().st_mtime)

                    saves.append(SaveFile(
                        slot=slot,
                        player_name=player_name,
                        day=day,
                        last_modified=last_modified,
                        file_path=file_path
                    ))

        # Remove duplicates (keep the one with highest day number per slot)
        slot_map = {}
        for save in saves:
            if save.slot not in slot_map or save.day > slot_map[save.slot].day:
                slot_map[save.slot] = save

        # Return sorted by slot number
        return sorted(slot_map.values(), key=lambda x: x.slot)

    def _get_day_from_json(self, slot: int) -> Optional[int]:
        """
        Extract day number from save JSON file
        Returns the lastSnapShotDay value
        """
        json_files = [
            self.save_path / f"save{slot:04d}.json",  # save0008.json
            self.save_path / f"save{slot}.json",      # save8.json or save0.json
        ]

        for json_file in json_files:
            if json_file.exists():
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    # Extract lastSnapShotDay
                    day = data.get('lastSnapShotDay', None)
                    if day is not None:
                        return int(day)

                except (json.JSONDecodeError, IOError, KeyError, ValueError):
                    continue

        return None

    def _get_player_name(self, slot: int) -> str:
        """
        Extract player name from save JSON file
        Looks for uniquePlayersData.playerName
        Caches the result per slot
        """
        # Check cache first
        if slot in self._player_name_cache:
            return self._player_name_cache[slot]

        # Try to find and read the JSON file for this slot
        json_files = [
            self.save_path / f"save{slot:04d}.json",  # save0008.json
            self.save_path / f"save{slot}.json",      # save8.json
        ]

        for json_file in json_files:
            if json_file.exists():
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    # Extract uniquePlayersData[0].playerName
                    # uniquePlayersData is a list/array, not a dict
                    unique_players_data = data.get('uniquePlayersData', [])
                    if isinstance(unique_players_data, list) and len(unique_players_data) > 0:
                        player_name = unique_players_data[0].get('playerName', None)

                        if player_name:
                            self._player_name_cache[slot] = player_name
                            return player_name

                except (json.JSONDecodeError, IOError, KeyError, IndexError, TypeError):
                    # If we can't read the file, continue to next attempt
                    continue

        # Fallback if we couldn't find the name
        default_name = f"Player {slot}"
        self._player_name_cache[slot] = default_name
        return default_name

    def scan_backups(self, slot: Optional[int] = None) -> List[Backup]:
        """
        Scan the Backup folder for backup files
        If slot is provided, only return backups for that slot
        Returns sorted by date (newest first)
        """
        backups = []

        if not self.backup_path.exists():
            return backups

        for file_path in self.backup_path.iterdir():
            if file_path.is_file() and file_path.suffix == '.zip':
                # Extract slot and day from filename
                # Pattern: save0008_day_34.zip, save0008_current_20250103_1430.zip
                match = re.match(r'save(\d+)', file_path.name)
                if match:
                    backup_slot = int(match.group(1))

                    # Skip if filtering by slot and doesn't match
                    if slot is not None and backup_slot != slot:
                        continue

                    # Extract day if present
                    day_match = re.search(r'day[_\s](\d+)', file_path.name, re.IGNORECASE)
                    day = int(day_match.group(1)) if day_match else None

                    # Get file stats
                    stats = file_path.stat()
                    date = datetime.fromtimestamp(stats.st_mtime)
                    size = stats.st_size

                    backups.append(Backup(
                        filename=file_path.name,
                        slot=backup_slot,
                        day=day,
                        date=date,
                        file_path=file_path,
                        size_bytes=size
                    ))

        # Sort by date, newest first
        return sorted(backups, key=lambda x: x.date, reverse=True)

    def restore_backup(self, backup: Backup, progress_callback=None) -> bool:
        """
        Restore a backup file
        1. Create a safety backup of current state
        2. Extract the backup
        3. Replace current save files
        Returns True if successful, raises exception on error
        """
        try:
            # Step 1: Create safety backup
            if progress_callback:
                progress_callback("Creating safety backup of current state...")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safety_backup_name = f"save{backup.slot:04d}_current_{timestamp}.zip"
            safety_backup_path = self.backup_path / safety_backup_name

            # Create backup folder if it doesn't exist
            self.backup_path.mkdir(parents=True, exist_ok=True)

            # Zip current save files for this slot
            self._create_backup_for_slot(backup.slot, safety_backup_path)

            # Step 2: Extract backup to temp location
            if progress_callback:
                progress_callback("Extracting backup...")

            temp_dir = self.save_path / f"_temp_restore_{backup.slot}"
            temp_dir.mkdir(exist_ok=True)

            try:
                with zipfile.ZipFile(backup.file_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)

                # Step 3: Replace current save files
                if progress_callback:
                    progress_callback("Replacing save files...")

                # Find all files that match this slot
                for extracted_file in temp_dir.rglob('*'):
                    if extracted_file.is_file():
                        # Determine target path
                        relative_path = extracted_file.relative_to(temp_dir)
                        target_path = self.save_path / relative_path

                        # Create parent directories if needed
                        target_path.parent.mkdir(parents=True, exist_ok=True)

                        # Copy file
                        shutil.copy2(extracted_file, target_path)

                # Clear cache for this slot so player name gets re-read
                if backup.slot in self._player_name_cache:
                    del self._player_name_cache[backup.slot]

                if progress_callback:
                    progress_callback("Restore completed successfully!")

                return True

            finally:
                # Clean up temp directory
                if temp_dir.exists():
                    shutil.rmtree(temp_dir)

        except Exception as e:
            raise Exception(f"Failed to restore backup: {str(e)}")

    def create_backup(self, slot: int, day: int) -> Path:
        """
        Create a manual backup for the specified slot
        Returns the path to the created backup file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"save{slot:04d}_day_{day}_{timestamp}.zip"
        backup_path = self.backup_path / backup_name

        # Create backup folder if it doesn't exist
        self.backup_path.mkdir(parents=True, exist_ok=True)

        self._create_backup_for_slot(slot, backup_path)

        return backup_path

    def _create_backup_for_slot(self, slot: int, backup_path: Path):
        """
        Create a zip backup of all files for the given slot
        """
        # Find all files matching this slot
        slot_patterns = [
            f"save{slot:04d}.*",  # save0008.json, save0008.dat
            f"save{slot}.*",      # save8.json
        ]

        files_to_backup = []
        for pattern in slot_patterns:
            files_to_backup.extend(self.save_path.glob(pattern))

        if not files_to_backup:
            raise Exception(f"No save files found for slot {slot}")

        # Create zip file
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in files_to_backup:
                if file_path.is_file():
                    # Store with relative path
                    arcname = file_path.name
                    zipf.write(file_path, arcname)

    def validate_save_path(self) -> bool:
        """Check if the save path exists and is accessible"""
        return self.save_path.exists() and self.save_path.is_dir()
