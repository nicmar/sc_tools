"""
Data models for Space Chef Save Manager
"""
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
from typing import Optional


@dataclass
class SaveFile:
    """Represents a save file"""
    slot: int
    player_name: str
    day: int
    last_modified: datetime
    file_path: Path

    def __str__(self):
        return f"{self.player_name} (Slot {self.slot}) - Day {self.day}"

    def display_name(self):
        """Returns formatted display name for UI"""
        return f"{self.player_name} (Slot {self.slot}) - Day {self.day}"


@dataclass
class Backup:
    """Represents a backup file"""
    filename: str
    slot: int
    day: Optional[int]
    date: datetime
    file_path: Path
    size_bytes: int

    def display_date(self):
        """Returns formatted date for display"""
        return self.date.strftime("%b %d, %Y %H:%M")

    def display_size(self):
        """Returns human-readable file size"""
        size = self.size_bytes
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

    def display_day(self):
        """Returns formatted day string"""
        if self.day is not None:
            return f"Day {self.day}"
        return "N/A"
