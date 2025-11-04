#!/bin/zsh
# Launch script for Space Chef Save Manager on macOS

# Try Homebrew Python 3.13 first (has working Tkinter)
if [ -f "/opt/homebrew/bin/python3.13" ]; then
    /opt/homebrew/bin/python3.13 main.py
# Try Homebrew Python 3
elif [ -f "/opt/homebrew/bin/python3" ]; then
    /opt/homebrew/bin/python3 main.py
# Try system Python
elif [ -f "/usr/bin/python3" ]; then
    /usr/bin/python3 main.py
# Fall back to python3 in PATH
elif command -v python3 &> /dev/null; then
    python3 main.py
else
    echo "Error: Python 3 not found"
    exit 1
fi
