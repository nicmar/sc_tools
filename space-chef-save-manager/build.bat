@echo off
REM Build script for Windows

echo ========================================================================
echo   Space Chef Save Manager - Build Script (Windows)
echo ========================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found!
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo Using Python:
python --version
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo PyInstaller not found. Installing...
    python -m pip install pyinstaller
    echo.
)

REM Clean previous build
echo Cleaning previous build...
python build.py clean
echo.

REM Build executable
echo Building executable...
python build.py
if %ERRORLEVEL% NEQ 0 (
    echo Build failed!
    pause
    exit /b 1
)
echo.

REM Create package
echo Creating distribution package...
python package.py
if %ERRORLEVEL% NEQ 0 (
    echo Packaging failed!
    pause
    exit /b 1
)
echo.

echo ========================================================================
echo   Build Complete!
echo ========================================================================
echo.
echo Check the dist\ folder for the packaged zip file.
echo.
pause
