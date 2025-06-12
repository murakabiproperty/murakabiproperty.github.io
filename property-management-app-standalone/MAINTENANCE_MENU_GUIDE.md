# 🔧 Panduan Menu Maintenance/Repair

## 📍 **Di Mana Menemukan Menu Maintenance?**

Setelah menginstall Property Management System, Anda dapat mengakses menu maintenance/repair di beberapa lokasi:

### **1. Windows Start Menu** ⭐ **(REKOMENDASI)**

**📂 Start Menu → All Programs → Property Management System → Maintenance**

Anda akan menemukan:
- 🔧 **Repair Installation** - Perbaiki instalasi yang bermasalah
- ⚙️ **Modify Installation** - Ubah komponen yang terinstall

### **2. Windows Control Panel**

**🎛️ Control Panel → Programs → Programs and Features**
1. Cari "Property Management System" dalam daftar
2. Klik kanan → pilih **"Change"**
3. Pilih opsi maintenance yang diinginkan

### **3. Windows Settings (Windows 10/11)**

**⚙️ Settings → Apps → Apps & features**
1. Cari "Property Management System"
2. Klik → **"Modify"** atau **"Advanced options"**
3. Pilih **"Repair"** atau **"Modify"**

### **4. Direct Access (Manual)**

Jika installer tersimpan di direktori aplikasi:
```
C:\Program Files\Property Management System\PropertyManagementSystem_Setup_Maintenance.exe
```

## 🎯 **Opsi Maintenance yang Tersedia**

### **🔧 Repair Mode**
- **Kapan digunakan**: Ketika aplikasi tidak berfungsi dengan baik
- **Apa yang dilakukan**:
  - ✅ Memperbaiki file yang corrupt/hilang
  - ✅ Reset konfigurasi ke default
  - ✅ Reinstall dependencies Python
  - ✅ Membuat ulang shortcut dan registry entries

### **⚙️ Modify Mode**
- **Kapan digunakan**: Ketika ingin mengubah komponen instalasi
- **Apa yang dilakukan**:
  - ✅ Tambah/hapus komponen tertentu
  - ✅ Update debug tools
  - ✅ Update dokumentasi
  - ✅ Ubah shortcut desktop

### **🗑️ Uninstall**
- **Kapan digunakan**: Ketika ingin menghapus aplikasi sepenuhnya
- **Apa yang dilakukan**:
  - ✅ Hapus semua file aplikasi
  - ✅ Hapus registry entries
  - ✅ Hapus shortcuts
  - ⚠️ **Database dan gambar properti akan dihapus**

## 🚨 **Automatic Maintenance Detection**

Ketika Anda menjalankan installer dan aplikasi sudah terinstall, installer akan:

1. **Deteksi instalasi existing**
2. **Tampilkan dialog pilihan**:
   ```
   Property Management System is already installed.
   
   What would you like to do?
   
   Yes    = Repair/Reinstall (recommended)
   No     = Modify installation  
   Cancel = Exit setup
   ```
3. **Pilih sesuai kebutuhan**

## 📋 **Skenario Penggunaan**

### **🔴 Masalah Aplikasi Tidak Bisa Dibuka**
1. **Start Menu** → **Maintenance** → **Repair Installation**
2. Atau: **Control Panel** → **Programs** → **Change** → **Repair**

### **🟡 Aplikasi Berjalan Tapi Ada Error**
1. Coba gunakan **Debug Tools** dulu
2. Jika masih bermasalah: **Repair Installation**

### **🟢 Ingin Update/Tambah Fitur**
1. **Start Menu** → **Maintenance** → **Modify Installation**
2. Pilih komponen yang ingin ditambah/hapus

### **🔵 Database Corrupt/Hilang**
1. **Repair Installation** (akan reset database)
2. ⚠️ **Backup data penting sebelumnya**

## 🛠️ **Troubleshooting Maintenance**

### **Menu Maintenance Tidak Muncul di Start Menu**
1. **Reinstall** dengan installer terbaru
2. **Run as Administrator**
3. Check di **All Programs** → **Property Management System**

### **Control Panel Tidak Menampilkan Opsi Change**
1. **Run installer original** lagi
2. Pilih **Repair** saat dialog muncul

### **Error Saat Repair**
1. **Run as Administrator**
2. **Temporary disable** antivirus
3. **Check disk space** (minimal 100MB free)

## 🔍 **Verifikasi Instalasi**

Setelah repair/modify, pastikan:
- ✅ Aplikasi bisa dibuka normal
- ✅ Database terbaca dengan baik
- ✅ Debug tools berfungsi
- ✅ Shortcut di Start Menu ada

## 📞 **Support**

Jika masih mengalami masalah:
1. **Gunakan Debug Tools** untuk diagnosis
2. **Check log files** di direktori logs/
3. **Screenshot error message** yang muncul
4. **Hubungi support** dengan informasi lengkap

---

## 🎯 **Quick Access Commands**

```bash
# Via Start Menu
Start → Property Management System → Maintenance → Repair Installation

# Via Control Panel  
Control Panel → Programs → Property Management System → Change

# Via Settings (Windows 10/11)
Settings → Apps → Property Management System → Modify → Repair
``` 