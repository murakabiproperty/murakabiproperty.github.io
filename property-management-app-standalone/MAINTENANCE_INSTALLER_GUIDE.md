# 🔧 Property Management System - Maintenance Mode Installer Guide

## 📦 Installer Overview

### Available Installers:

1. **PropertyManagementSystem_Setup_Maintenance.exe** ⭐ **TERBARU** (9:48 PM)
   - **Maintenance Mode** dengan deteksi instalasi otomatis
   - **Opsi Repair, Modify, Reinstall** saat aplikasi sudah terinstall
   - **Uninstall via Control Panel**

2. **PropertyManagementSystem_Setup_Basic.exe** (9:21 PM)
   - Basic installer tanpa maintenance mode

3. **PropertyManagementSystem_Setup_Simple.exe** (8:48 PM)
   - Simple installer versi sebelumnya

## 🚀 Cara Menggunakan Maintenance Mode Installer

### 📥 **Instalasi Pertama Kali**

1. **Double-click** `PropertyManagementSystem_Setup_Maintenance.exe`
2. **Follow wizard** instalasi normal
3. **Pilih opsi yang diinginkan**:
   - ✅ Create Desktop Icon
   - ✅ Create Start Menu entry
   - ⚪ Start with Windows (optional)
4. **Click Install** untuk melanjutkan

### 🔄 **Ketika Aplikasi Sudah Terinstall**

Ketika menjalankan installer dan aplikasi sudah terinstall, installer akan **otomatis mendeteksi** dan menampilkan:

#### **Welcome Screen yang Berbeda:**
```
Property Management System is already installed.

This installer can repair, modify, or reinstall the application.
To uninstall, please use "Add or Remove Programs" from Control Panel.

Click Next to continue, or Cancel to exit.
```

#### **Maintenance Options:**
Pada halaman **Select Components**, Anda akan melihat opsi:

🔧 **Maintenance Mode:**
- **⚪ Repair installation** - Reinstall semua file program
- **⚪ Modify installation** - Ubah komponen yang terinstall
- **⚪ Reinstall application** - Instalasi ulang lengkap

🎯 **Additional Options:**
- **☑️ Create Desktop Icon**
- **☑️ Create Start Menu entry** 
- **⚪ Start with Windows**

### 🛠️ **Fungsi Masing-masing Mode:**

#### 1. **🔧 Repair Installation**
- **Tujuan**: Memperbaiki instalasi yang rusak
- **Yang dilakukan**:
  - ✅ Reinstall semua file aplikasi
  - ✅ Restore registry entries
  - ✅ Fix file permissions
  - ✅ Restore desktop shortcuts
- **Kapan digunakan**: File aplikasi hilang/rusak, shortcut tidak bekerja

#### 2. **⚙️ Modify Installation**
- **Tujuan**: Mengubah komponen yang terinstall
- **Yang dilakukan**:
  - ✅ Add/remove optional components
  - ✅ Change startup settings
  - ✅ Update shortcuts
- **Kapan digunakan**: Ingin mengubah opsi instalasi tanpa reinstall

#### 3. **🔄 Reinstall Application**
- **Tujuan**: Instalasi ulang lengkap
- **Yang dilakukan**:
  - ✅ Complete fresh installation
  - ✅ Update semua file ke versi terbaru
  - ✅ Reset semua settings
- **Kapan digunakan**: Update ke versi baru atau reset lengkap

### 🗑️ **Uninstall Application**

Untuk **menghapus aplikasi**, gunakan:

#### **Method 1: Control Panel**
1. **Open Control Panel** → Programs → Uninstall a program
2. **Find** "Property Management System"
3. **Click Uninstall** dan follow instructions

#### **Method 2: Start Menu**
1. **Open Start Menu** → Property Management System folder
2. **Click** "Uninstall Property Management System"
3. **Follow** uninstall wizard

## ✨ **Fitur Advanced Maintenance Installer**

### 🔍 **Automatic Detection**
- ✅ Deteksi instalasi existing otomatis
- ✅ Registry check untuk verifikasi
- ✅ File path validation

### 🛡️ **Safety Features**
- ✅ **Backup protection** - Tidak menghapus database user
- ✅ **Process termination** - Otomatis tutup aplikasi sebelum update
- ✅ **Registry cleanup** saat uninstall
- ✅ **Temp files cleanup**

### 📋 **User Experience**
- ✅ **Dynamic welcome message** berdasarkan status instalasi
- ✅ **Context-aware options** 
- ✅ **Professional wizard interface**
- ✅ **Informative progress tracking**

## 🎯 **Best Practices**

### ✅ **Recommended Usage:**
1. **Tutup aplikasi** sebelum menjalankan maintenance
2. **Backup database** jika diperlukan (file `property_management.db`)
3. **Gunakan "Repair"** untuk masalah kecil
4. **Gunakan "Reinstall"** untuk update major

### ⚠️ **Important Notes:**
- Database user **TIDAK akan dihapus** saat repair/reinstall
- Settings dan gambar properti **akan dipertahankan**
- Untuk uninstall complete, gunakan Control Panel
- Administrator privileges **diperlukan** untuk instalasi

## 🆘 **Troubleshooting**

### **Installer tidak jalan:**
- Run as Administrator
- Disable antivirus sementara
- Check Windows compatibility

### **Repair tidak berhasil:**
- Coba Reinstall mode
- Manual uninstall kemudian install fresh
- Check disk space dan permissions

### **Database hilang setelah reinstall:**
- Check backup di folder user documents
- Restore dari `property_management_backup.db`

---

## 📞 **Support**

Jika mengalami masalah, silakan check:
1. **Error logs** di folder aplikasi
2. **Windows Event Viewer** untuk error details
3. **File permissions** di installation directory

**Installation Directory:** `C:\Program Files\Property Management System\` 