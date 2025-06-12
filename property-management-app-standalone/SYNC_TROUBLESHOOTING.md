# Panduan Troubleshooting Sinkronisasi Airtable

## Masalah Umum dan Solusi

### 1. Error "Sinkronisasi Gagal" saat Edit Properti

**Gejala:** Muncul popup error "Properti berhasil diupdate di database lokal, tapi gagal disinkronkan ke Airtable."

**Cara Debug:**

1. **Jalankan Debug Script:**
   ```
   python debug_edit_sync.py
   ```

2. **Lihat Log Error Terbaru:**
   ```
   python view_sync_errors.py
   ```

3. **Test Koneksi Manual:**
   ```
   python test_status_sync.py
   ```

### 2. Kemungkinan Penyebab

#### A. Record Airtable Tidak Ditemukan
- Record mungkin sudah dihapus dari Airtable
- Airtable Record ID di database sudah tidak valid

**Solusi:**
- Buka Airtable dan cek apakah record masih ada
- Jika record hilang, hapus dan tambah ulang properti

#### B. Masalah Koneksi Internet
- Koneksi internet terputus
- Firewall memblokir akses ke Airtable

**Solusi:**
- Cek koneksi internet
- Test koneksi dengan script: `python test_status_sync.py`

#### C. Konfigurasi Airtable Salah
- API Key tidak valid
- Base ID atau Table ID salah

**Solusi:**
- Cek file `airtable_config.py`
- Pastikan semua kredensial benar

### 3. Menggunakan Enhanced Logging

Aplikasi sekarang memiliki sistem logging yang lebih baik:

#### File Log yang Dibuat:
- `logs/app_YYYYMMDD.log` - Log aplikasi umum
- `logs/airtable_sync_YYYYMMDD.log` - Log khusus sinkronisasi Airtable

#### Cara Melihat Log:
```bash
# Lihat error sync terbaru
python view_sync_errors.py

# Lihat log aplikasi
python view_sync_errors.py --app
```

### 4. Debug Step-by-Step

1. **Reproduksi Masalah:**
   - Buka aplikasi
   - Coba edit properti yang ada Airtable Record ID
   - Catat detail error

2. **Jalankan Debug:**
   ```
   python debug_edit_sync.py
   ```

3. **Analisis Output:**
   - Apakah koneksi Airtable berhasil?
   - Apakah record ditemukan di Airtable?
   - Apa pesan error detail?

4. **Check Log Files:**
   ```
   python view_sync_errors.py
   ```

### 5. Solusi Berdasarkan Error

#### Error: "Record not found"
- Record sudah dihapus dari Airtable
- **Solusi:** Hapus properti dari database lokal dan tambah ulang

#### Error: "Invalid API key"
- Kredensial Airtable salah
- **Solusi:** Update `airtable_config.py` dengan kredensial yang benar

#### Error: "Network timeout"
- Masalah koneksi internet
- **Solusi:** Cek koneksi internet dan coba lagi

#### Error: "Permission denied"
- API key tidak memiliki permission untuk mengubah data
- **Solusi:** Cek permission API key di Airtable

### 6. Bantuan Lebih Lanjut

Jika masalah masih berlanjut:

1. Jalankan semua script debug
2. Kumpulkan informasi:
   - Screenshot error
   - Output dari `debug_edit_sync.py`
   - Log terbaru dari `view_sync_errors.py`
3. Hubungi dukungan teknis dengan informasi tersebut

### 7. Maintenance

**Pembersihan Log Berkala:**
- Log files akan bertambah setiap hari
- Hapus file log lama secara berkala
- File log biasanya berukuran kecil, aman untuk dihapus setelah beberapa minggu

**Update Koneksi:**
- Test koneksi Airtable secara berkala dengan `test_status_sync.py`
- Pastikan kredensial selalu up-to-date 