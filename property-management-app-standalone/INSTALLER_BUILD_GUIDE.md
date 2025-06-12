# Panduan Lengkap Membuat Ulang Installer

## 🚀 Cara Cepat (Otomatis)

### 1. Rebuild Installer (One Command)
```bash
python rebuild_installer.py
```

### 2. Compile Installer (One Command)
```bash
python compile_installer.py
```

## 📋 Persiapan

### Prerequisites
1. **Python 3.9+** harus terinstall
2. **PyInstaller** untuk membuat executable
3. **Inno Setup** untuk membuat installer

### Install Prerequisites
```bash
# Install PyInstaller
pip install pyinstaller

# Download dan install Inno Setup dari:
# https://jrsoftware.org/isinfo.php
```

## 🔧 Langkah Manual (Step by Step)

### Step 1: Persiapan Environment
```bash
# Pastikan di direktori property-management-app-standalone
cd property-management-app-standalone

# Install dependencies
pip install -r requirements.txt
pip install pyinstaller
```

### Step 2: Build Executable dengan PyInstaller
```bash
pyinstaller --onefile --windowed --name=PropertyManager --icon=app_icon.ico --add-data="airtable_sync.py;." --add-data="airtable_config.py;." --add-data="enhanced_logging.py;." --add-data="error_dialog.py;." --hidden-import=PIL._tkinter_finder --hidden-import=tkinter --hidden-import=tkinter.ttk --clean main.py
```

### Step 3: Prepare Installer Files
```bash
# Buat direktori installer jika belum ada
mkdir -p installer_files/app

# Copy executable ke installer directory
cp dist/PropertyManager.exe installer_files/app/

# Copy semua Python scripts untuk debug tools
cp *.py installer_files/app/

# Copy documentation
cp *.md installer_files/app/

# Copy assets
cp app_icon.ico installer_files/app/
```

### Step 4: Create Inno Setup Script
Buat file `installer_files/PropertyManagementSystem_Setup.iss` (sudah disediakan oleh `rebuild_installer.py`)

### Step 5: Compile dengan Inno Setup
```bash
# Option 1: Otomatis
python compile_installer.py

# Option 2: Manual
# 1. Buka Inno Setup Compiler
# 2. Load file: installer_files/PropertyManagementSystem_Setup.iss
# 3. Klik "Compile"
```

## 📦 Fitur Installer yang Dihasilkan

### Main Application
- ✅ Executable utama (`PropertyManager.exe`)
- ✅ Database dan konfigurasi
- ✅ Direktori untuk gambar dan logs

### Debug Tools (Menu Start)
- 🔧 **Test Airtable Sync** - Test koneksi dan sync Airtable
- 🔧 **Debug Edit Sync** - Debug masalah edit properti
- 🔧 **View Error Logs** - Lihat log error terbaru

### Documentation (Menu Start)
- 📚 **User Manual** - Panduan penggunaan
- 📚 **Troubleshooting Guide** - Panduan troubleshooting
- 📚 **Airtable Integration Guide** - Panduan integrasi Airtable

### Auto-Installation Features
- ✅ Check Python installation
- ✅ Install Python packages otomatis
- ✅ Create required directories
- ✅ Set proper permissions

## 🗂️ Struktur File Installer

```
installer_files/
├── PropertyManagementSystem_Setup.iss    # Inno Setup script
├── PropertyManagementSystem_Setup_Enhanced.exe  # Final installer
├── wizard_image.bmp                      # Installer wizard image
├── wizard_small.bmp                      # Small wizard image
└── app/
    ├── PropertyManager.exe               # Main application
    ├── main.py                          # Source Python script
    ├── airtable_sync.py                 # Airtable sync module
    ├── airtable_config.py               # Configuration
    ├── enhanced_logging.py              # Enhanced logging
    ├── error_dialog.py                  # Enhanced error dialog
    ├── debug_edit_sync.py               # Debug tool
    ├── view_sync_errors.py              # Log viewer
    ├── test_status_sync.py              # Connection test
    ├── requirements.txt                 # Python dependencies
    ├── app_icon.ico                     # Application icon
    ├── USER_MANUAL.md                   # Documentation
    ├── SYNC_TROUBLESHOOTING.md          # Troubleshooting guide
    └── AIRTABLE_INTEGRATION_GUIDE.md    # Integration guide
```

## 🎯 Version Information

- **Version**: 2.1.0 (Enhanced)
- **Features**: 
  - Enhanced error handling dan logging
  - Debug tools terintegrasi
  - Comprehensive documentation
  - Auto-dependency installation

## 🔍 Troubleshooting Build Issues

### Error: "PyInstaller not found"
```bash
pip install pyinstaller
```

### Error: "Inno Setup not found"
- Download dari: https://jrsoftware.org/isinfo.php
- Install dengan default settings

### Error: "Module not found"
```bash
# Install missing modules
pip install requests pillow

# Atau install semua dependencies
pip install -r requirements.txt
```

### Error: "Permission denied"
- Run Command Prompt as Administrator
- Atau ubah destination directory

### Build Errors dengan PyInstaller
```bash
# Clean previous builds
rm -rf build/ dist/ *.spec

# Rebuild
python rebuild_installer.py
```

## ⚡ Quick Commands Cheat Sheet

```bash
# Full rebuild (everything in one command)
python rebuild_installer.py && python compile_installer.py

# Clean and rebuild
rm -rf build/ dist/ *.spec installer_files/app/ && python rebuild_installer.py

# Just compile (if installer files already ready)
python compile_installer.py

# Test the created installer
.\installer_files\PropertyManagementSystem_Setup_Enhanced.exe
```

## 📊 Expected Output

Setelah berhasil build, Anda akan mendapatkan:

1. **Installer File**: `PropertyManagementSystem_Setup_Enhanced.exe` (~12-15 MB)
2. **Debug Tools**: Accessible via Start Menu
3. **Documentation**: Terintegrasi dalam installer
4. **Auto-Setup**: Python dependencies terinstall otomatis

## 🚀 Distribution

Installer yang dihasilkan dapat didistribusikan dan akan:
- ✅ Install aplikasi ke `Program Files`
- ✅ Create Start Menu shortcuts
- ✅ Setup debug tools
- ✅ Install Python dependencies
- ✅ Create desktop shortcut (opsional)
- ✅ Register uninstaller

## 📞 Support

Jika mengalami masalah saat build installer:

1. Check Python version: `python --version`
2. Check PyInstaller: `pyinstaller --version`
3. Check Inno Setup installation
4. Review error messages di console
5. Gunakan `rebuild_installer.py` untuk build otomatis 