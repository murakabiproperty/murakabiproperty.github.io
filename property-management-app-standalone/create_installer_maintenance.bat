@echo off
echo.
echo =============================================
echo   Creating Maintenance Mode Installer
echo =============================================
echo.

echo 📦 Building executable...
python build_installer.py

echo.
echo 📁 Checking installer files...
if not exist "installer_files\app\PropertyManager.exe" (
    echo ❌ ERROR: PropertyManager.exe not found in installer_files\app\
    echo Please run build_installer.py first
    pause
    exit /b 1
)

echo ✅ Executable found: installer_files\app\PropertyManager.exe

echo.
echo 🔧 Creating maintenance mode installer...
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "installer_script_maintenance.iss"
    if %errorlevel% equ 0 (
        echo.
        echo ✅ Maintenance installer created successfully: PropertyManagementSystem_Setup_Maintenance.exe
        echo.
        echo 🎯 Features:
        echo   • Detects existing installation
        echo   • Repair option - reinstalls all files
        echo   • Modify option - change components
        echo   • Uninstall option - complete removal
        echo   • Reinstall option - fresh installation
        echo.
        dir PropertyManagementSystem_Setup_Maintenance.exe
    ) else (
        echo ❌ Error creating maintenance installer
        pause
        exit /b 1
    )
) else (
    echo ❌ ERROR: Inno Setup 6 not found in C:\Program Files (x86)\Inno Setup 6\
    echo Please install Inno Setup 6 from: https://jrsoftware.org/isinfo.php
    pause
    exit /b 1
)

echo.
echo ✅ Process completed!
pause 