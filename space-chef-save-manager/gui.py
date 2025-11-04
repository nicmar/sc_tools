"""
Simplified GUI with pack layout for better compatibility
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import platform
import subprocess
import os
from typing import Optional, List
from config import Config
from save_manager import SaveManager
from models import SaveFile, Backup


class SaveManagerGUI:
    """Main GUI window for Space Chef Save Manager"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(f"{Config.APP_NAME} v{Config.VERSION}")
        self.root.geometry("750x600")
        self.root.minsize(650, 500)

        # Initialize save manager with default path
        default_path = Config.get_default_save_path()
        self.save_path = default_path if default_path.exists() else Path.cwd()
        self.save_manager = SaveManager(self.save_path)

        # Data
        self.saves: List[SaveFile] = []
        self.selected_save: Optional[SaveFile] = None

        # Build GUI
        self._create_widgets()
        self._load_saves()

    def _create_widgets(self):
        """Create all GUI widgets using pack layout"""

        # Save Location Section
        location_frame = ttk.LabelFrame(self.root, text="Save Location", padding="10")
        location_frame.pack(fill=tk.X, padx=10, pady=10)

        path_container = ttk.Frame(location_frame)
        path_container.pack(fill=tk.X)

        self.path_var = tk.StringVar(value=str(self.save_path))
        path_entry = ttk.Entry(path_container, textvariable=self.path_var)
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        browse_btn = ttk.Button(path_container, text="Browse...", command=self._browse_folder)
        browse_btn.pack(side=tk.LEFT, padx=2)

        open_folder_btn = ttk.Button(path_container, text="📁 Open", command=self._open_save_folder)
        open_folder_btn.pack(side=tk.LEFT, padx=2)

        # Player Selection Section
        selection_frame = ttk.LabelFrame(self.root, text="Select a Player/Save", padding="10")
        selection_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # List with scrollbar
        list_frame = ttk.Frame(selection_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.saves_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=('TkDefaultFont', 11),
            height=12
        )
        self.saves_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.saves_listbox.yview)
        self.saves_listbox.bind('<<ListboxSelect>>', self._on_save_selected)

        # Action Buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.view_backups_btn = ttk.Button(
            button_frame,
            text="View Backups",
            command=self._view_backups,
            state=tk.DISABLED,
            width=15
        )
        self.view_backups_btn.pack(side=tk.LEFT, padx=5)

        self.create_backup_btn = ttk.Button(
            button_frame,
            text="Create Backup",
            command=self._create_backup,
            state=tk.DISABLED,
            width=15
        )
        self.create_backup_btn.pack(side=tk.LEFT, padx=5)

        refresh_btn = ttk.Button(button_frame, text="Refresh", command=self._load_saves, width=12)
        refresh_btn.pack(side=tk.LEFT, padx=5)

        # Utility Buttons
        utility_frame = ttk.Frame(self.root)
        utility_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        open_saves_btn = ttk.Button(utility_frame, text="Open Save Folder", command=self._open_save_folder, width=18)
        open_saves_btn.pack(side=tk.LEFT, padx=5)

        open_logs_btn = ttk.Button(utility_frame, text="Open Player Logs", command=self._open_logs_folder, width=18)
        open_logs_btn.pack(side=tk.LEFT, padx=5)

        # Status bar
        status_frame = ttk.Frame(self.root, relief=tk.SUNKEN, borderwidth=1)
        status_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, anchor=tk.W)
        status_label.pack(fill=tk.X, padx=5, pady=2)

    def _load_saves(self):
        """Load and display save files"""
        try:
            # Update save path from entry field
            new_path = Path(self.path_var.get())
            if new_path != self.save_path:
                self.save_path = new_path
                self.save_manager = SaveManager(self.save_path)

            # Check if path is valid
            if not self.save_manager.validate_save_path():
                self.status_var.set(f"Error: Save path does not exist")
                messagebox.showwarning("Path Not Found", f"The save path does not exist:\n{self.save_path}")
                return

            # Load saves
            self.saves = self.save_manager.scan_saves()

            # Update UI
            self.saves_listbox.delete(0, tk.END)

            if self.saves:
                for save in self.saves:
                    self.saves_listbox.insert(tk.END, save.display_name())
                self.status_var.set(f"Found {len(self.saves)} save file(s)")
            else:
                self.saves_listbox.insert(tk.END, "No save files found")
                self.status_var.set("No save files found")

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Error loading saves:\n{error_details}")
            messagebox.showerror("Error", f"Failed to load saves: {str(e)}")
            self.status_var.set("Error loading saves")

    def _on_save_selected(self, event):
        """Handle save selection from listbox"""
        selection = self.saves_listbox.curselection()
        if selection and self.saves:
            index = selection[0]
            if index < len(self.saves):
                self.selected_save = self.saves[index]
                self._update_button_states()

    def _update_button_states(self):
        """Enable/disable buttons based on selection"""
        if self.selected_save:
            self.view_backups_btn.config(state=tk.NORMAL)
            self.create_backup_btn.config(state=tk.NORMAL)
        else:
            self.view_backups_btn.config(state=tk.DISABLED)
            self.create_backup_btn.config(state=tk.DISABLED)

    def _browse_folder(self):
        """Open folder picker dialog"""
        folder = filedialog.askdirectory(
            title="Select Space Chef Saves Folder",
            initialdir=str(self.save_path)
        )
        if folder:
            self.path_var.set(folder)
            self._load_saves()

    def _open_save_folder(self):
        """Open the save folder in file explorer"""
        self._open_folder(self.save_path)

    def _open_logs_folder(self):
        """Open the player logs folder"""
        logs_path = Config.get_logs_path()
        self._open_folder(logs_path)

    def _open_folder(self, path: Path):
        """Open folder in system file explorer"""
        if not path.exists():
            messagebox.showwarning("Folder Not Found", f"The folder does not exist:\n{path}")
            return

        try:
            system = platform.system()
            if system == "Windows":
                os.startfile(path)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", str(path)])
            else:  # Linux
                subprocess.run(["xdg-open", str(path)])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open folder: {str(e)}")

    def _view_backups(self):
        """Open backup viewer window"""
        if not self.selected_save:
            return

        BackupWindow(self.root, self.save_manager, self.selected_save, self._load_saves)

    def _create_backup(self):
        """Create a manual backup of the selected save"""
        if not self.selected_save:
            return

        try:
            result = messagebox.askyesno(
                "Create Backup",
                f"Create a backup of:\n{self.selected_save.display_name()}?"
            )

            if result:
                backup_path = self.save_manager.create_backup(
                    self.selected_save.slot,
                    self.selected_save.day
                )
                messagebox.showinfo(
                    "Success",
                    f"Backup created successfully:\n{backup_path.name}"
                )
                self.status_var.set("Backup created successfully")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create backup: {str(e)}")


class BackupWindow:
    """Window for viewing and restoring backups"""

    def __init__(self, parent: tk.Tk, save_manager: SaveManager, save_file: SaveFile, refresh_callback):
        self.save_manager = save_manager
        self.save_file = save_file
        self.refresh_callback = refresh_callback

        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title(f"Backups for {save_file.display_name()}")
        self.window.geometry("750x450")
        self.window.transient(parent)
        self.window.grab_set()

        self.backups: List[Backup] = []
        self.selected_backup: Optional[Backup] = None

        self._create_widgets()
        self._load_backups()

    def _create_widgets(self):
        """Create backup window widgets"""

        # Info label
        info_label = ttk.Label(
            self.window,
            text=f"Available backups for: {self.save_file.display_name()}",
            font=('TkDefaultFont', 11, 'bold'),
            padding=10
        )
        info_label.pack()

        # Backup list with treeview
        tree_frame = ttk.Frame(self.window)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=('date', 'filename', 'day', 'size'),
            show='headings',
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)

        # Define columns
        self.tree.heading('date', text='Date')
        self.tree.heading('filename', text='Filename')
        self.tree.heading('day', text='Day')
        self.tree.heading('size', text='Size')

        self.tree.column('date', width=150)
        self.tree.column('filename', width=300)
        self.tree.column('day', width=100)
        self.tree.column('size', width=100)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self._on_backup_selected)

        # Info label
        info_note = ttk.Label(
            self.window,
            text="ℹ️  Note: Your current save will be automatically backed up before restoring",
            foreground="#4A90E2",
            padding=10
        )
        info_note.pack()

        # Buttons
        button_frame = ttk.Frame(self.window)
        button_frame.pack(pady=10)

        self.restore_btn = ttk.Button(
            button_frame,
            text="Restore Selected",
            command=self._restore_backup,
            state=tk.DISABLED,
            width=18
        )
        self.restore_btn.pack(side=tk.LEFT, padx=5)

        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self.window.destroy, width=12)
        cancel_btn.pack(side=tk.LEFT, padx=5)

    def _load_backups(self):
        """Load backups for the selected save slot"""
        try:
            self.backups = self.save_manager.scan_backups(slot=self.save_file.slot)

            # Clear tree
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Populate tree
            if self.backups:
                for backup in self.backups:
                    self.tree.insert('', tk.END, values=(
                        backup.display_date(),
                        backup.filename,
                        backup.display_day(),
                        backup.display_size()
                    ))
            else:
                # Show message if no backups
                self.tree.insert('', tk.END, values=(
                    'No backups found',
                    '',
                    '',
                    ''
                ))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load backups: {str(e)}")

    def _on_backup_selected(self, event):
        """Handle backup selection"""
        selection = self.tree.selection()
        if selection and self.backups:
            index = self.tree.index(selection[0])
            if index < len(self.backups):
                self.selected_backup = self.backups[index]
                self.restore_btn.config(state=tk.NORMAL)

    def _restore_backup(self):
        """Restore the selected backup"""
        if not self.selected_backup:
            return

        # Confirm with user
        result = messagebox.askyesnocancel(
            "Confirm Restore",
            f"Restore backup from {self.selected_backup.display_date()}?\n\n"
            f"This will restore: {self.selected_backup.display_day()}\n\n"
            f"Your current save will be backed up automatically before restoring."
        )

        if not result:
            return

        # Create progress dialog
        progress_window = tk.Toplevel(self.window)
        progress_window.title("Restoring...")
        progress_window.geometry("400x120")
        progress_window.transient(self.window)
        progress_window.grab_set()

        progress_label = ttk.Label(progress_window, text="Preparing restore...", padding=20)
        progress_label.pack()

        progress_bar = ttk.Progressbar(progress_window, mode='indeterminate', length=300)
        progress_bar.pack(pady=10)
        progress_bar.start()

        def progress_callback(message):
            progress_label.config(text=message)
            progress_window.update()

        # Perform restore
        def do_restore():
            try:
                self.save_manager.restore_backup(self.selected_backup, progress_callback)
                progress_window.destroy()
                messagebox.showinfo("Success", "Backup restored successfully!")
                self.refresh_callback()  # Refresh main window
                self.window.destroy()
            except Exception as e:
                progress_window.destroy()
                messagebox.showerror("Error", f"Failed to restore backup: {str(e)}")

        # Run restore after a short delay to allow UI to update
        self.window.after(100, do_restore)
