#!/usr/bin/env python3
"""
Script untuk compile installer Inno Setup secara otomatis
"""

import os
import subprocess
import sys
from pathlib import Path
import winreg

def find_inno_setup():
    """Find Inno Setup Compiler installation"""
    
    # Common installation paths
    common_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
        r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
        r"C:\Program Files\Inno Setup 5\ISCC.exe",
    ]
    
    # Check common paths first
    for path in common_paths:
        if Path(path).exists():
            return path
    
    # Try to find via registry
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall") as key:
            for i in range(winreg.QueryInfoKey(key)[0]):
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    with winreg.OpenKey(key, subkey_name) as subkey:
                        try:
                            display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            if "Inno Setup" in display_name:
                                install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                                iscc_path = Path(install_location) / "ISCC.exe"
                                if iscc_path.exists():
                                    return str(iscc_path)
                        except FileNotFoundError:
                            continue
                except OSError:
                    continue
    except Exception:
        pass
    
    return None

def compile_installer():
    """Compile the Inno Setup installer"""
    print("🔨 Compiling Property Management System Installer")
    print("=" * 60)
    
    # Find Inno Setup Compiler
    iscc_path = find_inno_setup()
    
    if not iscc_path:
        print("❌ Inno Setup Compiler not found!")
        print("\nPlease install Inno Setup from: https://jrsoftware.org/isinfo.php")
        print("Or run the installer script manually:")
        print("1. Open Inno Setup Compiler")
        print("2. Load: installer_files/PropertyManagementSystem_Setup.iss")
        print("3. Click 'Compile'")
        return False
    
    print(f"✅ Found Inno Setup Compiler: {iscc_path}")
    
    # Check if installer script exists (try simple version first)
    script_path = Path("installer_files/PropertyManagementSystem_Setup_Simple.iss")
    if not script_path.exists():
        script_path = Path("installer_files/PropertyManagementSystem_Setup.iss")
        if not script_path.exists():
            print(f"❌ Installer script not found: {script_path}")
            print("Please run 'python rebuild_installer.py' first")
            return False
    
    print(f"✅ Found installer script: {script_path}")
    
    # Compile the installer
    try:
        print("\n🔄 Compiling installer...")
        result = subprocess.run([
            iscc_path,
            str(script_path.absolute())
        ], capture_output=True, text=True, check=True)
        
        print("✅ Compilation successful!")
        
        # Look for the created installer
        installer_path = Path("installer_files/PropertyManagementSystem_Setup_Enhanced.exe")
        if installer_path.exists():
            size_mb = installer_path.stat().st_size / (1024 * 1024)
            print(f"📦 Installer created: {installer_path.name} ({size_mb:.1f} MB)")
            print(f"📁 Location: {installer_path.absolute()}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Compilation failed!")
        print(f"Error output: {e.stderr}")
        return False
    
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def main():
    """Main function"""
    success = compile_installer()
    
    if success:
        print("\n🎉 Installer compilation completed successfully!")
        print("\nYou can now distribute the installer:")
        print("📦 installer_files/PropertyManagementSystem_Setup_Enhanced.exe")
    else:
        print("\n❌ Installer compilation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 