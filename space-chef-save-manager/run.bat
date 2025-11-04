@echo off
REM Launch script for Space Chef Save Manager on Windows

python main.py
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to launch application
    pause
)
