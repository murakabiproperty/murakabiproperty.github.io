@echo off
echo ============================================
echo Property Management System Uninstaller
echo ============================================
echo.

set /p confirm="Are you sure you want to uninstall Property Management System? (y/n): "
if /i not "%confirm%"=="y" (
    echo Uninstallation cancelled.
    pause
    exit /b 0
)

echo.
echo Uninstalling Property Management System...

REM Remove desktop shortcut
set DESKTOP=%USERPROFILE%\Desktop
if exist "%DESKTOP%\Property Manager.lnk" (
    echo Removing desktop shortcut...
    del "%DESKTOP%\Property Manager.lnk"
)

REM Remove virtual environment
if exist "property_manager_env" (
    echo Removing virtual environment...
    rmdir /s /q property_manager_env
)

REM Remove launcher script
if exist "run_property_manager.bat" (
    echo Removing launcher script...
    del run_property_manager.bat
)

REM Ask about database
echo.
set /p keep_db="Do you want to keep your property database? (y/n): "
if /i not "%keep_db%"=="y" (
    if exist "property_management.db" (
        echo Removing database...
        del property_management.db
    )
) else (
    echo Database preserved at: property_management.db
)

echo.
echo ============================================
echo Uninstallation completed!
echo ============================================
echo.
echo The Property Management System has been uninstalled.
echo You can safely delete this folder if you no longer need it.
echo.
pause 