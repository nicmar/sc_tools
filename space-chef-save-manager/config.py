"""
Configuration module for Space Chef Save Manager
Handles platform-specific paths and constants
"""
import platform
import os
from pathlib import Path


class Config:
    """Configuration class for platform-specific settings"""

    APP_NAME = "Space Chef Save Manager"
    VERSION = "1.0.1"

    @staticmethod
    def get_default_save_path() -> Path:
        """Get the default save location based on platform

        Intelligently detects the correct path by checking multiple locations
        and preferring the one that contains actual save files.
        """
        system = platform.system()

        if system == "Windows":
            # Windows: Check multiple possible locations
            userprofile = os.environ.get('USERPROFILE', '')
            appdata_roaming = os.environ.get('APPDATA', '')

            possible_paths = []

            # Primary location: LocalLow (Unity default)
            if userprofile:
                locallow_path = Path(userprofile) / "AppData" / "LocalLow" / "BlueGooGames" / "Space Chef" / "Saves"
                possible_paths.append(locallow_path)

            # Secondary location: Roaming (alternative configuration)
            if appdata_roaming:
                roaming_path = Path(appdata_roaming) / "BlueGooGames" / "Space Chef" / "Saves"
                possible_paths.append(roaming_path)

            # Return the first path that contains .json files, or the first path that exists
            for path in possible_paths:
                if path.exists():
                    # Check if it has save files (.json)
                    if any(path.glob("save*.json")):
                        return path

            # If no path has saves, return the first one that exists
            for path in possible_paths:
                if path.exists():
                    return path

            # If nothing exists, return the primary path (LocalLow)
            if possible_paths:
                return possible_paths[0]

        elif system == "Darwin":  # macOS
            # Mac: ~/Library/Application Support/BlueGooGames/Space Chef/Saves
            home = Path.home()
            return home / "Library" / "Application Support" / "BlueGooGames" / "Space Chef" / "Saves"

        elif system == "Linux":
            # Linux: ~/.local/share/BlueGooGames/Space Chef/Saves (XDG standard)
            home = Path.home()
            return home / ".local" / "share" / "BlueGooGames" / "Space Chef" / "Saves"

        # Fallback to current directory if platform not recognized
        return Path.cwd()

    @staticmethod
    def get_logs_path() -> Path:
        """Get the player logs location based on platform"""
        system = platform.system()

        if system == "Windows":
            # Windows: %USERPROFILE%\AppData\LocalLow\BlueGooGames\Space Chef
            userprofile = os.environ.get('USERPROFILE', '')
            if userprofile:
                return Path(userprofile) / "AppData" / "LocalLow" / "BlueGooGames" / "Space Chef"

        elif system == "Darwin":  # macOS
            # Mac: ~/Library/Logs/BlueGooGames/Space Chef (standard Mac logs location)
            home = Path.home()
            return home / "Library" / "Logs" / "BlueGooGames" / "Space Chef"

        elif system == "Linux":
            # Linux: ~/.local/share/BlueGooGames/Space Chef/logs
            home = Path.home()
            return home / ".local" / "share" / "BlueGooGames" / "Space Chef" / "logs"

        return Path.cwd()

    @staticmethod
    def get_backup_folder(save_path: Path) -> Path:
        """Get the backup folder relative to save path"""
        return save_path / "Backup"
