#!/usr/bin/env python3
"""
Build Script for Property Management Application
Creates a standalone executable and prepares installer files
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def install_requirements():
    """Install required packages for building"""
    required_packages = [
        'cx_Freeze',
        'requests',
        'urllib3',
        'certifi',
        'charset-normalizer',
        'idna',
        'Pillow'
    ]
    
    for package in required_packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✓ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {package}")
            return False
    return True

def clean_build_directory():
    """Clean previous build artifacts"""
    build_dirs = ['build', 'dist', 'installer_files']
    
    for dir_name in build_dirs:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✓ Cleaned {dir_name} directory")

def create_cx_freeze_setup():
    """Create setup.py for cx_Freeze"""
    setup_content = '''
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it's better to be explicit
build_options = {
    'packages': ['tkinter', 'sqlite3', 'requests', 'urllib3', 'urllib3.util', 'urllib3.exceptions', 'urllib3.poolmanager', 'http', 'http.client', 'http.server', 'http.cookies', 'http.cookiejar', 'certifi', 'charset_normalizer', 'idna', 'PIL', 'pathlib', 'json', 'hashlib', 'datetime', 'os', 'shutil', 'webbrowser', 'urllib', 'urllib.parse', 'urllib.request', 'urllib.response', 'urllib.error', 'mimetypes'],
    'excludes': ['test', 'unittest', 'email', 'html', 'xml', 'pydoc'],
    'include_files': [
        ('airtable_config.py', 'airtable_config.py'),
        ('airtable_sync.py', 'airtable_sync.py'),
        ('AIRTABLE_INTEGRATION_GUIDE.md', 'AIRTABLE_INTEGRATION_GUIDE.md'),
        ('USER_MANUAL.md', 'USER_MANUAL.md'),
        ('requirements.txt', 'requirements.txt'),
        ('app_icon.ico', 'app_icon.ico')
    ],
    'optimize': 2
}

# GUI applications require a different base on Windows
base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable(
        'main.py',
        base=base,
        target_name='PropertyManager.exe',
        icon='app_icon.ico',
        shortcut_name='Property Management System',
        shortcut_dir='DesktopFolder'
    )
]

setup(
    name='Property Management System',
    version='1.0.0',
    description='Desktop Property Management Application with Airtable Integration',
    author='Property Management Team',
    options={'build_exe': build_options},
    executables=executables
)
'''
    
    with open('setup_freeze.py', 'w') as f:
        f.write(setup_content)
    print("✓ Created cx_Freeze setup file")

def build_executable():
    """Build the executable using cx_Freeze"""
    try:
        subprocess.check_call([sys.executable, 'setup_freeze.py', 'build'])
        print("✓ Built executable successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to build executable")
        return False

def prepare_installer_files():
    """Prepare files for the installer"""
    installer_dir = Path('installer_files')
    installer_dir.mkdir(exist_ok=True)
    
    # Copy built executable
    build_dir = Path('build')
    exe_dir = None
    for item in build_dir.iterdir():
        if item.is_dir() and item.name.startswith('exe.'):
            exe_dir = item
            break
    
    if exe_dir:
        shutil.copytree(exe_dir, installer_dir / 'app')
        print("✓ Copied executable files")
    else:
        print("✗ Could not find built executable")
        return False
    
    # Copy additional files
    additional_files = [
        'AIRTABLE_INTEGRATION_GUIDE.md',
        'USER_MANUAL.md',
        'install.bat',
        'uninstall.bat',
        'app_icon.ico',
        'wizard_image.bmp',
        'wizard_small.bmp'
    ]
    
    for file_name in additional_files:
        if os.path.exists(file_name):
            shutil.copy2(file_name, installer_dir)
            print(f"✓ Copied {file_name}")
    
    return True

def main():
    """Main build process"""
    print("🏗️  Building Property Management Application Installer")
    print("=" * 50)
    
    # Step 1: Install requirements
    print("\n📦 Installing build requirements...")
    if not install_requirements():
        print("❌ Failed to install requirements")
        return
    
    # Step 2: Clean previous builds
    print("\n🧹 Cleaning build directory...")
    clean_build_directory()
    
    # Step 3: Create setup file
    print("\n📝 Creating build configuration...")
    create_cx_freeze_setup()
    
    # Step 4: Build executable
    print("\n🔨 Building executable...")
    if not build_executable():
        return
    
    # Step 5: Prepare installer files
    print("\n📁 Preparing installer files...")
    if not prepare_installer_files():
        return
    
    print("\n✅ Build completed successfully!")
    print("📂 Files ready in 'installer_files' directory")
    print("🚀 Ready to create installer with Inno Setup")

if __name__ == "__main__":
    main() 