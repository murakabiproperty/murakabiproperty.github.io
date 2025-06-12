#!/usr/bin/env python3
"""
Script untuk rebuild installer Property Management System
dengan semua update terbaru termasuk enhanced logging dan debug tools
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path
from datetime import datetime

def print_step(step_num, message):
    """Print step with formatting"""
    print(f"\n🔧 Step {step_num}: {message}")
    print("=" * 60)

def copy_file_with_log(src, dst, description=""):
    """Copy file with logging"""
    try:
        shutil.copy2(src, dst)
        print(f"✅ Copied: {src.name} {description}")
        return True
    except Exception as e:
        print(f"❌ Failed to copy {src.name}: {str(e)}")
        return False

def rebuild_installer():
    """Rebuild the installer with latest updates"""
    print("🚀 Rebuilding Property Management System Installer")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Paths
    base_dir = Path(".")
    installer_dir = base_dir / "installer_files"
    app_dir = installer_dir / "app"
    
    print_step(1, "Preparing installer directories")
    
    # Create installer directories if they don't exist
    installer_dir.mkdir(exist_ok=True)
    app_dir.mkdir(exist_ok=True)
    
    print_step(2, "Building executable with PyInstaller")
    
    # Check if PyInstaller is available
    try:
        result = subprocess.run([sys.executable, "-m", "PyInstaller", "--version"], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ PyInstaller not found. Installing...")
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    except Exception as e:
        print(f"❌ Error with PyInstaller: {e}")
        print("Please install PyInstaller: pip install pyinstaller")
        return False
    
    # PyInstaller command
    pyinstaller_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=PropertyManager",
        "--icon=app_icon.ico",
        "--add-data=airtable_sync.py;.",
        "--add-data=airtable_config.py;.",
        "--add-data=enhanced_logging.py;.",
        "--add-data=error_dialog.py;.",
        "--hidden-import=PIL._tkinter_finder",
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.ttk",
        "--clean",
        "main.py"
    ]
    
    try:
        print("Building executable...")
        result = subprocess.run(pyinstaller_cmd, check=True, capture_output=True, text=True)
        print("✅ Executable built successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ PyInstaller failed: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False
    
    print_step(3, "Copying main application files")
    
    # Copy main executable
    exe_source = base_dir / "dist" / "PropertyManager.exe"
    if exe_source.exists():
        copy_file_with_log(exe_source, app_dir / "PropertyManager.exe", "(main executable)")
    else:
        print("❌ Executable not found!")
        return False
    
    # Copy Python scripts (for debug and maintenance)
    python_files = [
        "main.py",
        "airtable_sync.py", 
        "airtable_config.py",
        "enhanced_logging.py",
        "error_dialog.py",
        "debug_edit_sync.py",
        "view_sync_errors.py",
        "test_status_sync.py"
    ]
    
    for file in python_files:
        src_file = base_dir / file
        if src_file.exists():
            copy_file_with_log(src_file, app_dir / file, "(Python script)")
    
    print_step(4, "Copying documentation and guides")
    
    # Copy documentation files
    doc_files = [
        "SYNC_TROUBLESHOOTING.md",
        "AIRTABLE_INTEGRATION_GUIDE.md", 
        "USER_MANUAL.md"
    ]
    
    for file in doc_files:
        src_file = base_dir / file
        if src_file.exists():
            copy_file_with_log(src_file, app_dir / file, "(documentation)")
        else:
            # Try in installer_files directory
            installer_file = installer_dir / file
            if installer_file.exists():
                copy_file_with_log(installer_file, app_dir / file, "(documentation)")
    
    print_step(5, "Copying additional files")
    
    # Copy icon and other assets
    asset_files = ["app_icon.ico"]
    for file in asset_files:
        src_file = base_dir / file
        if src_file.exists():
            copy_file_with_log(src_file, app_dir / file, "(asset)")
    
    # Copy requirements.txt
    requirements_content = """requests==2.31.0
Pillow==10.0.1
"""
    with open(app_dir / "requirements.txt", "w") as f:
        f.write(requirements_content)
    print("✅ Created: requirements.txt")
    
    print_step(6, "Creating installer script")
    
    # Create updated Inno Setup script
    create_inno_script(installer_dir)
    
    print_step(7, "Cleaning up build files")
    
    # Clean up PyInstaller build files
    build_dirs = ["build", "dist", "__pycache__"]
    for dir_name in build_dirs:
        build_dir = base_dir / dir_name
        if build_dir.exists():
            try:
                shutil.rmtree(build_dir)
                print(f"✅ Cleaned: {dir_name}/")
            except:
                print(f"⚠️  Could not clean: {dir_name}/")
    
    # Remove .spec file
    spec_file = base_dir / "PropertyManager.spec"
    if spec_file.exists():
        try:
            spec_file.unlink()
            print("✅ Cleaned: PropertyManager.spec")
        except:
            print("⚠️  Could not clean: PropertyManager.spec")
    
    print_step(8, "Installer ready!")
    
    print("🎉 Installer rebuild completed!")
    print(f"📁 Installer files location: {installer_dir.absolute()}")
    print("\nNext steps:")
    print("1. Open Inno Setup Compiler")
    print("2. Load the script: installer_files/PropertyManagementSystem_Setup.iss")
    print("3. Compile to create the installer")
    print("\nOr run: python compile_installer.py")
    
    return True

def create_inno_script(installer_dir):
    """Create updated Inno Setup script"""
    app_dir = installer_dir / "app"
    
    inno_script = f'''
; Property Management System - Enhanced Installer Script
; Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
; Includes enhanced logging, debug tools, and error handling

#define MyAppName "Property Management System"
#define MyAppVersion "2.1.0"
#define MyAppPublisher "Property Management Solutions"
#define MyAppURL "https://github.com/yourusername/property-management"
#define MyAppExeName "PropertyManager.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
AppId={{7B8F9E2C-1D3A-4F5E-9B7A-8C6D5E4F3A2B}}
AppName={{#MyAppName}}
AppVersion={{#MyAppVersion}}
AppPublisher={{#MyAppPublisher}}
AppPublisherURL={{#MyAppURL}}
AppSupportURL={{#MyAppURL}}
AppUpdatesURL={{#MyAppURL}}
DefaultDirName={{autopf}}\\{{#MyAppName}}
DefaultGroupName={{#MyAppName}}
AllowNoIcons=yes
LicenseFile=
OutputDir=.
OutputBaseFilename=PropertyManagementSystem_Setup_Enhanced
SetupIconFile=app\\app_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
WizardImageFile=wizard_image.bmp
WizardSmallImageFile=wizard_small.bmp
DisableProgramGroupPage=yes
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "indonesian"; MessagesFile: "compiler:Languages\\Indonesian.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked

[Files]
; Main application
Source: "app\\PropertyManager.exe"; DestDir: "{{app}}"; Flags: ignoreversion

; Python scripts for debugging and maintenance
Source: "app\\*.py"; DestDir: "{{app}}"; Flags: ignoreversion

; Documentation and guides
Source: "app\\*.md"; DestDir: "{{app}}"; Flags: ignoreversion

; Configuration and requirements
Source: "app\\requirements.txt"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "app\\app_icon.ico"; DestDir: "{{app}}"; Flags: ignoreversion

; Create directories
[Dirs]
Name: "{{app}}\\logs"; Permissions: users-full
Name: "{{app}}\\property_images"; Permissions: users-full

[Icons]
Name: "{{group}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"
Name: "{{group}}\\{{cm:UninstallProgram,{{#MyAppName}}}}"; Filename: "{{uninstallexe}}"
Name: "{{autodesktop}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"; Tasks: desktopicon

; Debug and maintenance tools
Name: "{{group}}\\Debug Tools\\Test Airtable Sync"; Filename: "{{sys}}\\cmd.exe"; Parameters: "/c cd /d ""{{app}}"" && python test_status_sync.py && pause"; WorkingDir: "{{app}}"
Name: "{{group}}\\Debug Tools\\Debug Edit Sync"; Filename: "{{sys}}\\cmd.exe"; Parameters: "/c cd /d ""{{app}}"" && python debug_edit_sync.py && pause"; WorkingDir: "{{app}}"
Name: "{{group}}\\Debug Tools\\View Error Logs"; Filename: "{{sys}}\\cmd.exe"; Parameters: "/c cd /d ""{{app}}"" && python view_sync_errors.py && pause"; WorkingDir: "{{app}}"
Name: "{{group}}\\Documentation\\User Manual"; Filename: "{{app}}\\USER_MANUAL.md"
Name: "{{group}}\\Documentation\\Troubleshooting Guide"; Filename: "{{app}}\\SYNC_TROUBLESHOOTING.md"
Name: "{{group}}\\Documentation\\Airtable Integration Guide"; Filename: "{{app}}\\AIRTABLE_INTEGRATION_GUIDE.md"

[Run]
Filename: "{{app}}\\{{#MyAppExeName}}"; Description: "{{cm:LaunchProgram,{{#StringChange(MyAppName, '&', '&&')}}}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{{app}}\\logs"
Type: filesandordirs; Name: "{{app}}\\property_images"
Type: files; Name: "{{app}}\\property_management.db"

[Code]
function InitializeSetup(): Boolean;
var
  PythonInstalled: Boolean;
  ResultCode: Integer;
begin
  // Check if Python is installed
  PythonInstalled := RegKeyExists(HKEY_LOCAL_MACHINE, 'SOFTWARE\\Python\\PythonCore\\3.11') or
                     RegKeyExists(HKEY_CURRENT_USER, 'SOFTWARE\\Python\\PythonCore\\3.11') or
                     RegKeyExists(HKEY_LOCAL_MACHINE, 'SOFTWARE\\Python\\PythonCore\\3.10') or
                     RegKeyExists(HKEY_CURRENT_USER, 'SOFTWARE\\Python\\PythonCore\\3.10') or
                     RegKeyExists(HKEY_LOCAL_MACHINE, 'SOFTWARE\\Python\\PythonCore\\3.9') or
                     RegKeyExists(HKEY_CURRENT_USER, 'SOFTWARE\\Python\\PythonCore\\3.9');
  
  if not PythonInstalled then
  begin
    if MsgBox('Python 3.9+ is required for debug tools to work properly. The main application will work without Python, but debug tools will not be available.' + #13#10#13#10 + 'Do you want to continue with the installation?', mbConfirmation, MB_YESNO) = IDNO then
    begin
      Result := False;
      Exit;
    end;
  end;
  
  Result := True;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
  PythonExe: String;
begin
  if CurStep = ssPostInstall then
  begin
    // Try to find Python executable
    PythonExe := 'python';
    
    // Install required packages if Python is available
    if Exec('cmd', '/c python --version', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) and (ResultCode = 0) then
    begin
      // Install required packages
      Exec('cmd', '/c cd /d "' + ExpandConstant('{{app}}') + '" && python -m pip install -r requirements.txt', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
    end;
  end;
end;
'''
    
    # Write the Inno Setup script
    script_path = installer_dir / "PropertyManagementSystem_Setup.iss"
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(inno_script)
    
    print(f"✅ Created: {script_path.name}")

if __name__ == "__main__":
    success = rebuild_installer()
    if success:
        print("\n✅ Installer rebuild completed successfully!")
    else:
        print("\n❌ Installer rebuild failed!")
        sys.exit(1) 