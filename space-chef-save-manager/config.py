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
    VERSION = "1.0.0"

    @staticmethod
    def get_default_save_path() -> Path:
        """Get the default save location based on platform"""
        system = platform.system()

        if system == "Windows":
            # Windows: %AppData%\BlueGooGames\Space Chef\Saves
            appdata = os.environ.get('APPDATA', '')
            if appdata:
                return Path(appdata) / "BlueGooGames" / "Space Chef" / "Saves"

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
