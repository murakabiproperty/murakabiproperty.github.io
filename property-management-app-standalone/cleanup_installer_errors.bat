@echo off
echo =============================================
echo Property Management System - Complete Cleanup
echo =============================================
echo.
echo This script will completely clean all traces of
echo Property Management System to fix installer errors.
echo.
echo WARNING: This will remove ALL data including:
echo - Application files
echo - Database
echo - Images  
echo - Configuration
echo - Registry entries
echo.
set /p confirm="Are you sure you want to continue? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo Cleanup cancelled.
    pause
    exit /b 0
)

echo.
echo Starting complete cleanup...
echo.

:: Stop any running processes
echo Stopping Property Management System processes...
taskkill /f /im PropertyManager.exe 2>nul
taskkill /f /im PropertyManagementSystem.exe 2>nul
timeout /t 2 >nul

:: Remove registry entries
echo Cleaning registry entries...
reg delete "HKCU\Software\PropertyManagementSystem" /f 2>nul
reg delete "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\Property Management System_is1" /f 2>nul
reg delete "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\PropertyManagementSystem_is1" /f 2>nul

:: Remove installation directories
echo Removing installation directories...
rmdir /s /q "C:\Program Files\Property Management System" 2>nul
rmdir /s /q "C:\Program Files (x86)\Property Management System" 2>nul

:: Remove user data directories
echo Removing user data directories...
rmdir /s /q "%APPDATA%\PropertyManagementSystem" 2>nul
rmdir /s /q "%LOCALAPPDATA%\PropertyManagementSystem" 2>nul
rmdir /s /q "%USERPROFILE%\Documents\PropertyManagementSystem" 2>nul

:: Remove shortcuts
echo Removing shortcuts...
del "%USERPROFILE%\Desktop\Property Management System.lnk" 2>nul
del "%PUBLIC%\Desktop\Property Management System.lnk" 2>nul
del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Property Management System.lnk" 2>nul
del "%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs\Property Management System.lnk" 2>nul

:: Remove start menu folder
rmdir /s /q "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Property Management System" 2>nul
rmdir /s /q "%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs\Property Management System" 2>nul

:: Clean temporary files
echo Cleaning temporary files...
del /q "%TEMP%\PropertyManagement*.*" 2>nul
del /q "%TEMP%\Inno Setup*.*" 2>nul

:: Clear installer cache
echo Clearing installer cache...
rmdir /s /q "%TEMP%\is-*" 2>nul

echo.
echo =============================================
echo Cleanup completed successfully!
echo =============================================
echo.
echo All Property Management System files and
echo registry entries have been removed.
echo.
echo You can now safely install using the new
echo safe installer: PropertyManagementSystem_Setup_Safe.exe
echo.
echo Recommendations:
echo 1. Restart your computer
echo 2. Run the new installer as Administrator
echo 3. Use build_installer_safe.bat for future builds
echo.
pause 