#!/usr/bin/env python3
"""
Space Chef Save Manager
Main entry point for the application
"""
import os

# Suppress macOS Tk deprecation warning
os.environ['TK_SILENCE_DEPRECATION'] = '1'

import tkinter as tk
from gui import SaveManagerGUI


def main():
    """Main entry point"""
    root = tk.Tk()

    # Create and run the GUI
    app = SaveManagerGUI(root)

    # Start the main loop
    root.mainloop()


if __name__ == "__main__":
    main()
