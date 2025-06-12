# Property Management System - Installer Creation Guide

This guide explains how to create a professional Windows installer for the Property Management System.

## 🎯 Overview

The installer system creates a complete Windows setup package that:
- Bundles the Python application into a standalone executable
- Creates a professional installation wizard
- Handles Airtable configuration during installation
- Sets up shortcuts, file associations, and registry entries
- Provides a complete uninstaller

## 📋 Prerequisites

### For Building the Installer:
1. **Python 3.7+** with pip
2. **Inno Setup 6** - Download from [jrsoftware.org](https://jrsoftware.org/isdl.php)
3. **Windows 7+** (for building and testing)

### Python Dependencies:
- `cx_Freeze` - Converts Python to executable
- `requests` - For Airtable API
- `Pillow` - Image processing

## 🔨 Build Process

### Automated Build (Recommended)

Simply run the automated builder:
```cmd
create_installer.bat
```

This will:
1. Install required Python packages
2. Build the executable
3. Create the installer package
4. Output: `PropertyManagementSystem_Setup.exe`

### Manual Build Process

#### Step 1: Prepare Environment
```cmd
pip install cx_Freeze requests Pillow
```

#### Step 2: Build Executable
```cmd
python build_installer.py
```

#### Step 3: Create Installer
Open `installer_script.iss` in Inno Setup and compile, or use command line:
```cmd
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer_script.iss
```

## 📁 File Structure

```
property-management-app-standalone/
├── 📄 main.py                     # Main application
├── 📄 airtable_sync.py           # Airtable integration
├── 📄 airtable_config.py         # Configuration
├── 🔧 build_installer.py         # Build script
├── 🔧 installer_script.iss       # Inno Setup script
├── 🔧 create_installer.bat       # Automated builder
├── 📄 INSTALL_INFO.txt          # Installation info
├── 📄 LICENSE.txt               # License file
├── 📖 USER_MANUAL.md            # User documentation
├── 📖 AIRTABLE_INTEGRATION_GUIDE.md # Setup guide
└── 📁 installer_files/          # Build output
    └── 📁 app/                  # Built executable
```

## ⚙️ Installer Features

### Professional Installation Wizard
- **Welcome Page** - Introduction and system requirements
- **License Agreement** - MIT license terms
- **Installation Path** - Customizable install directory
- **Airtable Configuration** - Guided credential setup
- **Components Selection** - Choose what to install
- **Progress Display** - Real-time installation progress
- **Completion Page** - Launch options and next steps

### Automatic Configuration
- **Registry Entries** - Application settings and paths
- **File Associations** - .pmdb files open with the app
- **Shortcuts** - Desktop and Start Menu entries
- **Environment Setup** - Application data directories

### Smart Features
- **Prerequisite Checking** - Validates system requirements
- **Credential Validation** - Checks Airtable API inputs
- **Upgrade Support** - Handles application updates
- **Clean Uninstallation** - Complete removal with data options

## 🎛️ Customization Options

### Branding
Edit `installer_script.iss`:
```pascal
AppName=Your Property Management System
AppPublisher=Your Company Name
SetupIconFile=your_icon.ico
WizardImageFile=your_banner.bmp
```

### Installation Options
```pascal
DefaultDirName={autopf}\Your App Name
PrivilegesRequired=admin
```

### File Associations
```pascal
Root: HKCR; Subkey: ".youtext"; ValueData: "YourFileType"
```

## 🧪 Testing the Installer

### Test Scenarios
1. **Fresh Installation** - Clean system install
2. **Upgrade Installation** - Install over existing version
3. **Configuration Test** - Airtable credential setup
4. **Uninstallation Test** - Complete removal
5. **Offline Installation** - Install without internet

### Validation Checklist
- [ ] Application launches correctly
- [ ] Airtable sync works with provided credentials
- [ ] All shortcuts function properly
- [ ] File associations work
- [ ] Uninstaller removes everything cleanly
- [ ] No leftover files or registry entries

## 📦 Distribution

### Installer Output
The build process creates: `PropertyManagementSystem_Setup.exe`

### Distribution Options
1. **Direct Download** - Host on website
2. **Email Distribution** - Send to clients
3. **Network Deployment** - IT department distribution
4. **USB Distribution** - Offline installation media

### Digital Signing (Optional)
For professional distribution, consider code signing:
```cmd
signtool sign /f certificate.pfx /p password PropertyManagementSystem_Setup.exe
```

## 🛠️ Troubleshooting

### Common Build Issues

**Python Package Errors:**
```cmd
pip install --upgrade cx_Freeze requests Pillow
```

**Inno Setup Not Found:**
- Verify installation path
- Check both Program Files and Program Files (x86)
- Reinstall Inno Setup if necessary

**Build Failures:**
- Check Python version compatibility
- Ensure all source files are present
- Review build log for specific errors

### Installation Issues

**Permission Errors:**
- Run installer as Administrator
- Check antivirus software interference

**Configuration Problems:**
- Verify Airtable credentials
- Check internet connectivity
- Review configuration file syntax

## 🔧 Advanced Customization

### Adding New Components
Edit `installer_script.iss` [Files] section:
```pascal
Source: "new_file.txt"; DestDir: "{app}"; Flags: ignoreversion
```

### Custom Installation Pages
Add to [Code] section:
```pascal
procedure CreateCustomPage;
begin
  // Custom page logic
end;
```

### Registry Modifications
```pascal
Root: HKCU; Subkey: "Software\YourApp"; ValueType: string; ValueName: "Setting"; ValueData: "Value"
```

## 📊 Maintenance

### Version Updates
1. Update version numbers in `installer_script.iss`
2. Rebuild executable with new code
3. Test upgrade installation
4. Update documentation

### Configuration Changes
- Modify `airtable_config.py` for new defaults
- Update installer prompts as needed
- Test configuration validation

## 🎉 Success Metrics

A successful installer should:
- ✅ Install without user intervention (except configuration)
- ✅ Create working application immediately
- ✅ Provide clear error messages if issues occur
- ✅ Support both technical and non-technical users
- ✅ Leave no traces when uninstalled

---

## 📞 Support

For installer creation support:
1. Check build logs for specific errors
2. Verify all prerequisites are installed
3. Test on clean virtual machine
4. Review Inno Setup documentation

**The goal is one-click installation for end users! 🚀** 