@echo off
echo ============================================
echo Property Management System Installer
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python is installed.
echo.

REM Get current directory
set INSTALL_DIR=%~dp0
echo Installing to: %INSTALL_DIR%

REM Create virtual environment
echo Creating virtual environment...
python -m venv property_manager_env
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment and install dependencies
echo Activating virtual environment...
call property_manager_env\Scripts\activate.bat

REM Install required packages
echo Installing dependencies...
pip install --upgrade pip

REM Since tkinter is built-in, we only need to install additional packages if any
REM For now, we'll just use built-in modules

REM Create desktop shortcut
echo Creating desktop shortcut...
set DESKTOP=%USERPROFILE%\Desktop
set SHORTCUT_PATH=%DESKTOP%\Property Manager.lnk

REM Create a batch file to run the application
echo @echo off > run_property_manager.bat
echo cd /d "%INSTALL_DIR%" >> run_property_manager.bat
echo call property_manager_env\Scripts\activate.bat >> run_property_manager.bat
echo python main.py >> run_property_manager.bat
echo pause >> run_property_manager.bat

REM Create VBS script to create shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > create_shortcut.vbs
echo sLinkFile = "%SHORTCUT_PATH%" >> create_shortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> create_shortcut.vbs
echo oLink.TargetPath = "%INSTALL_DIR%run_property_manager.bat" >> create_shortcut.vbs
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> create_shortcut.vbs
echo oLink.Description = "Property Management System" >> create_shortcut.vbs
echo oLink.IconLocation = "%SystemRoot%\System32\shell32.dll,21" >> create_shortcut.vbs
echo oLink.Save >> create_shortcut.vbs

cscript create_shortcut.vbs >nul 2>&1
del create_shortcut.vbs

echo.
echo ============================================
echo Installation completed successfully!
echo ============================================
echo.
echo The Property Management System has been installed.
echo.
echo To run the application:
echo 1. Double-click "Property Manager" on your desktop, OR
echo 2. Run "run_property_manager.bat" from this folder
echo.
echo Default login credentials:
echo Username: admin
echo Password: admin123
echo.
echo IMPORTANT: Please change the default password after first login!
echo.
pause 