@echo off
echo.
echo ============================================
echo   Creating Property Management Installer
echo ============================================
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
echo 🔧 Creating installer with basic script...
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "installer_script_basic.iss"
    if %errorlevel% equ 0 (
        echo ✅ Installer created successfully: PropertyManagementSystem_Setup_Basic.exe
    ) else (
        echo ❌ Error creating installer with basic script
    )
) else (
    echo ❌ Inno Setup not found at expected location
    echo Please install Inno Setup 6 or update the path in this script
)

echo.
echo 🎉 Process completed!
pause 