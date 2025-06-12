# Property Management System

A comprehensive desktop application for managing properties with Airtable integration, image management, and Google Maps support.

## 🚀 Quick Installation

**For End Users:**
1. Download `PropertyManagementSystem_Setup.exe`
2. Double-click to install
3. Follow the wizard instructions
4. Enter your Airtable credentials when prompted
5. Start using the application!

## 📋 Features

✅ **Property Management** - Add, edit, delete properties  
✅ **Airtable Integration** - Automatic cloud synchronization  
✅ **Image Support** - Upload and manage property images  
✅ **Google Maps** - Location integration with map links  
✅ **User Management** - Admin and user roles  
✅ **Search & Filter** - Find properties quickly  
✅ **Professional UI** - Modern, intuitive interface  

## 🛠️ For Developers

### Building the Installer

**Prerequisites:**
- Python 3.7 or later
- [Inno Setup 6](https://jrsoftware.org/isdl.php)

**Steps:**
1. Clone the repository
2. Navigate to `property-management-app-standalone`
3. Run `create_installer.bat`
4. The installer will be created as `PropertyManagementSystem_Setup.exe`

### Manual Build Process

```bash
# Step 1: Install build dependencies
pip install cx_Freeze requests Pillow

# Step 2: Build the executable
python build_installer.py

# Step 3: Create installer with Inno Setup
# Open installer_script.iss in Inno Setup and compile
```

## 📁 Project Structure

```
property-management-app-standalone/
├── main.py                     # Main application
├── airtable_sync.py           # Airtable integration
├── airtable_config.py         # Configuration file
├── build_installer.py         # Build script
├── installer_script.iss       # Inno Setup script
├── create_installer.bat       # Automated builder
├── INSTALL_INFO.txt          # Pre-installation info
├── LICENSE.txt               # Software license
├── USER_MANUAL.md            # User documentation
└── AIRTABLE_INTEGRATION_GUIDE.md # Setup guide
```

## 🔧 Configuration

The installer will prompt for Airtable credentials:
- **API Key**: Your Airtable Personal Access Token
- **Base ID**: Your Airtable Base identifier

You can also configure these later by editing `airtable_config.py`

## 📖 User Guide

After installation, users can access:
- **User Manual**: Complete usage instructions
- **Integration Guide**: Airtable setup help
- **Application**: Start from desktop or start menu

## 🚀 Deployment

The created installer (`PropertyManagementSystem_Setup.exe`) is fully self-contained and can be distributed to end users. It includes:

- All required dependencies
- Automatic configuration
- Desktop shortcuts
- Start menu entries
- File associations
- Uninstaller

## 🛡️ System Requirements

- Windows 7 or later (64-bit recommended)
- 500MB free disk space
- Internet connection (for Airtable sync)
- Microsoft Visual C++ Redistributable (auto-detected)

## 📞 Support

For installation or usage issues:
1. Check the User Manual
2. Review the Integration Guide
3. Create an issue on GitHub

## 📄 License

MIT License - see LICENSE.txt for details

---

**Made with ❤️ for property management professionals**
