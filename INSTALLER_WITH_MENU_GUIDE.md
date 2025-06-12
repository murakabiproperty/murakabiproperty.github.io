# Property Management System - Installer dengan Menu Deteksi

## 🎯 Fitur Baru: Menu Installer Otomatis

Installer baru ini mengatasi masalah sebelumnya dan memberikan **menu pilihan lengkap** ketika aplikasi sudah terinstall.

---

## ✨ Fitur Installer Baru

### 🔍 **Deteksi Instalasi Otomatis**
- Mendeteksi instalasi yang sudah ada
- Mencari di registry dan direktori default
- Menampilkan informasi instalasi saat ini

### 📋 **Menu Pilihan Lengkap**
Ketika aplikasi sudah terinstall, installer akan menampilkan 4 opsi:

1. **🔄 Install/Upgrade** - Upgrade ke versi terbaru (preserves data)
2. **🔧 Repair Installation** - Perbaiki file yang rusak
3. **⚙️ Modify Installation** - Tambah/hapus komponen
4. **🗑️ Uninstall Application** - Hapus aplikasi

### 🛡️ **Data Safety**
- **Preserves database** saat upgrade/repair
- **Backup configuration** otomatis
- **User choice** untuk preserve data saat uninstall
- **No runtime errors** seperti installer sebelumnya

---

## 🚀 Cara Menggunakan

### **Build Installer dengan Menu**
```batch
# Jalankan script build khusus
build_installer_with_menu.bat
```

**Output**: `PropertyManagementSystem_Setup_WithMenu.exe`

### **Test Installer**
1. **Install pertama kali** - Normal installation wizard
2. **Jalankan installer lagi** - Menu pilihan akan muncul
3. **Pilih opsi yang diinginkan** (upgrade, repair, modify, uninstall)

---

## 📊 Perbandingan Installer

| Fitur | Safe Installer | **Menu Installer** |
|-------|---------------|-------------------|
| Runtime Error | ❌ Tidak ada | ❌ Tidak ada |
| Detect Installation | ❌ Tidak | ✅ **Ya** |
| Menu Options | ❌ Tidak | ✅ **4 Opsi** |
| Data Preservation | ✅ Basic | ✅ **Advanced** |
| Upgrade Support | ❌ Manual | ✅ **Otomatis** |
| Repair Function | ❌ Tidak | ✅ **Ya** |

---

## 🎭 Demo Menu Installer

### **Skenario 1: Fresh Install**
```
Property Management System Setup
├── Welcome
├── Select Components  
├── Choose Install Location
├── Ready to Install
└── Installation Complete
```

### **Skenario 2: Existing Installation Detected**
```
Property Management System Setup
├── Welcome
├── 🔍 Existing Installation Detected
│   📍 Location: C:\Program Files\Property Management System
│   📋 Version: 1.0.0
│   
│   What would you like to do?
│   ◉ Install/Upgrade - Install new version (recommended)
│   ○ Repair Installation - Fix corrupted files and settings  
│   ○ Modify Installation - Add or remove components
│   ○ Uninstall Application - Remove Property Management System
│
├── [Depends on selection]
└── Operation Complete
```

---

## 🔧 Installer Scripts Available

### 1. **Safe Installer** (No Menu)
- File: `installer_script_simple_safe.iss`
- Build: `build_installer_safe.bat`
- Output: `PropertyManagementSystem_Setup_Safe.exe`
- **Use case**: Masih ada error dengan installer lama

### 2. **Menu Installer** (Recommended)
- File: `installer_script_with_menu.iss`  
- Build: `build_installer_with_menu.bat`
- Output: `PropertyManagementSystem_Setup_WithMenu.exe`
- **Use case**: Production ready, user-friendly

### 3. **Fixed Installer** (Advanced)
- File: `installer_script_fixed.iss`
- Build: Manual
- **Use case**: Development/testing

---

## 📋 Fitur Detail Menu Options

### 🔄 **Install/Upgrade**
- ✅ Otomatis backup konfigurasi lama
- ✅ Preserve database dan images  
- ✅ Update ke versi terbaru
- ✅ Restore settings personal

### 🔧 **Repair Installation**
- ✅ Replace file yang corrupt
- ✅ Restore default settings
- ✅ Fix registry entries
- ✅ Repair shortcuts dan menu

### ⚙️ **Modify Installation**
- ✅ Add/remove optional components
- ✅ Change installation features
- ✅ Update shortcuts
- ✅ Modify file associations

### 🗑️ **Uninstall Application**
- ✅ Jalankan uninstaller original
- ✅ Clean removal process
- ✅ Option to preserve data
- ✅ Complete cleanup

---

## 🎯 Cara Kerja Deteksi

### **Method 1: Registry Check**
```
HKCU\Software\PropertyManagementSystem\InstallPath
HKCU\Software\PropertyManagementSystem\Version
```

### **Method 2: Default Directory**
```
C:\Program Files\Property Management System\PropertyManager.exe
```

### **Method 3: Program Files (x86)**
```
C:\Program Files (x86)\Property Management System\PropertyManager.exe
```

---

## 🛡️ Error Prevention

### **Safe Coding Practices**
- ✅ Try-catch blocks di semua functions
- ✅ Null pointer checks
- ✅ File existence validation
- ✅ Registry access error handling

### **Fallback Mechanisms**
- ✅ Continue jika deteksi gagal
- ✅ Default ke normal install
- ✅ Skip pages yang error
- ✅ Generic messages untuk failures

---

## 🚦 Testing Guidelines

### **Test Cases**
1. ✅ Fresh install pada clean system
2. ✅ Detect existing installation  
3. ✅ Upgrade dari versi lama
4. ✅ Repair corrupted installation
5. ✅ Modify components
6. ✅ Uninstall dengan preserve data
7. ✅ Uninstall tanpa preserve data
8. ✅ Install setelah preserve data uninstall

### **Error Scenarios**
1. ✅ Registry access denied
2. ✅ File permission errors
3. ✅ Disk space insufficient
4. ✅ Installation directory locked
5. ✅ Antivirus interference

---

## 🎉 Kesimpulan

**Menu Installer** memberikan pengalaman user yang jauh lebih baik:

✅ **Professional** - Menu options seperti software commercial  
✅ **User-friendly** - Clear choices untuk setiap scenario  
✅ **Safe** - No runtime errors + data preservation  
✅ **Complete** - Support upgrade, repair, modify, uninstall  
✅ **Automated** - Deteksi dan handling otomatis  

**Recommendation: Gunakan `build_installer_with_menu.bat` untuk semua distribusi!**

---

## 📞 Support

Jika mengalami masalah:
1. Cek log di console saat build
2. Verify Inno Setup 6 terinstall
3. Test di clean machine terlebih dahulu
4. Gunakan safe installer sebagai fallback 