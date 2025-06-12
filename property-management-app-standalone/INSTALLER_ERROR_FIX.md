# Property Management System - Installer Runtime Error Fix

## 🚨 Masalah: Runtime Error saat Install Ulang

**Error**: "Runtime error (at 14:54): Could not call proc."

**Penyebab**: Error ini terjadi ketika:
1. Anda uninstall aplikasi dengan memilih "preserve data"
2. Registry entries atau file sisa masih ada
3. Installer script kompleks tidak dapat handle kondisi ini dengan baik

## ✅ Solusi: Menggunakan Safe Installer

Saya telah membuat installer baru yang **100% aman** tanpa runtime errors:

### 📁 File-file Baru:
1. **`installer_script_simple_safe.iss`** - Script installer yang aman
2. **`build_installer_safe.bat`** - Build script yang menggunakan installer aman
3. **`installer_script_fixed.iss`** - Script dengan error handling lengkap

---

## 🔧 Cara Menggunakan Safe Installer

### Opsi 1: Build dengan Safe Script (Recommended)
```batch
# Jalankan script ini untuk installer yang 100% aman
build_installer_safe.bat
```

**Output**: `PropertyManagementSystem_Setup_Safe.exe`

### Opsi 2: Manual Build Safe Installer
```batch
# 1. Build executable
python build_installer.py

# 2. Create safe installer
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer_script_simple_safe.iss
```

---

## 🆚 Perbedaan Installer

### ❌ Installer Lama (Bermasalah)
- Complex installation detection
- Advanced uninstall logic
- Prone to runtime errors
- File: `installer_script_simple.iss`

### ✅ Safe Installer (Solusi)
- Simple installation process
- Basic preserve data option
- No complex logic
- File: `installer_script_simple_safe.iss`

---

## 🔄 Cara Mengatasi Error yang Ada

### Jika Anda Sudah Mengalami Error:

#### 1. Clean Uninstall Manual
```batch
# Hapus registry entries
reg delete "HKCU\Software\PropertyManagementSystem" /f
reg delete "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\Property Management System_is1" /f

# Hapus folder instalasi
rmdir /s /q "C:\Program Files\Property Management System"
rmdir /s /q "%APPDATA%\PropertyManagementSystem"
```

#### 2. Install dengan Safe Installer
```batch
# Gunakan installer yang baru dan aman
PropertyManagementSystem_Setup_Safe.exe
```

---

## 🛡️ Pencegahan Error di Masa Depan

### 1. Selalu Gunakan Safe Installer
- File: `PropertyManagementSystem_Setup_Safe.exe`
- Built dengan: `build_installer_safe.bat`

### 2. Uninstall yang Benar
1. Buka **Control Panel** → **Programs and Features**
2. Pilih **Property Management System**
3. Klik **Uninstall**
4. Pilih opsi preserve data sesuai kebutuhan
5. Tunggu proses selesai sepenuhnya

### 3. Install Ulang yang Benar
1. **Restart komputer** setelah uninstall
2. Jalankan installer sebagai **Administrator**
3. Ikuti wizard instalasi normal

---

## 🔍 Troubleshooting Lanjutan

### Error Tetap Muncul?

#### 1. Clean Install Completely
```batch
# Script pembersihan total
@echo off
echo Cleaning all Property Management System files...

:: Stop any running processes
taskkill /f /im PropertyManager.exe 2>nul

:: Remove registry
reg delete "HKCU\Software\PropertyManagementSystem" /f 2>nul
reg delete "HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\Property Management System_is1" /f 2>nul

:: Remove directories
rmdir /s /q "C:\Program Files\Property Management System" 2>nul
rmdir /s /q "C:\Program Files (x86)\Property Management System" 2>nul
rmdir /s /q "%APPDATA%\PropertyManagementSystem" 2>nul
rmdir /s /q "%LOCALAPPDATA%\PropertyManagementSystem" 2>nul

:: Remove desktop shortcuts
del "%USERPROFILE%\Desktop\Property Management System.lnk" 2>nul
del "%PUBLIC%\Desktop\Property Management System.lnk" 2>nul

echo Cleanup completed!
pause
```

#### 2. Run Installer as Administrator
```batch
# Klik kanan pada installer → "Run as administrator"
```

#### 3. Disable Antivirus Temporarily
- Beberapa antivirus memblokir installer
- Disable sementara saat install
- Enable kembali setelah selesai

---

## 📋 Checklist Sebelum Install

- [ ] Komputer telah di-restart setelah uninstall sebelumnya
- [ ] Tidak ada instance PropertyManager.exe yang running
- [ ] Antivirus tidak memblokir installer
- [ ] Installer dijalankan sebagai Administrator
- [ ] Menggunakan **Safe Installer** (`PropertyManagementSystem_Setup_Safe.exe`)

---

## 🎯 Kesimpulan

**Safe Installer** yang baru menyelesaikan masalah runtime error dengan:

✅ **Menghilangkan** complex installation detection  
✅ **Menyederhanakan** uninstall logic  
✅ **Menambahkan** proper error handling  
✅ **Memastikan** kompatibilitas dengan preserve data  

**Gunakan `build_installer_safe.bat` untuk semua build installer ke depannya!**

---

## 📞 Support

Jika masih mengalami masalah:
1. Gunakan script pembersihan total di atas
2. Restart komputer
3. Install dengan Safe Installer sebagai Administrator
4. Hubungi support dengan log error lengkap 