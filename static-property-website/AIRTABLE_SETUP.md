# Panduan Pengaturan Integrasi Airtable

## 📋 Langkah 1: Buat Base Airtable Anda

1. **Kunjungi [Airtable.com](https://airtable.com)** dan daftar/masuk
2. **Buat base baru** - Klik "Add a base" → "Start from scratch"
3. **Beri nama base Anda** - contoh: "Database Uni Property"
4. **Ubah nama tabel default** menjadi "Properties"

## 🏗️ Langkah 2: Atur Tabel Properties Anda

Buat kolom-kolom berikut di tabel Airtable Anda:

| Nama Kolom | Jenis Field | Deskripsi |
|-------------|------------|-------------|
| **Name** | Single line text | Nama properti (contoh: "Apartemen Modern") |
| **Location** | Single line text | Lokasi properti (contoh: "Pusat Kota") |
| **Area** | Number | Luas properti dalam m² (contoh: 120) |
| **Bedrooms** | Number | Jumlah kamar tidur (contoh: 2) |
| **Bathrooms** | Number | Jumlah kamar mandi (contoh: 2) |
| **Price** | Number | Harga dalam Rupiah (contoh: 3500000000) |
| **Image** | Attachment | Gambar properti |
| **Description** | Long text | Deskripsi detail opsional |
| **MapLink** | URL | Link Google Maps share untuk lokasi properti |
| **Sold** | Checkbox | Status terjual (centang jika sudah terjual) |

## 🔑 Langkah 3: Dapatkan Kredensial API Anda

### Dapatkan API Key Anda:
1. Kunjungi [airtable.com/account](https://airtable.com/account)
2. Scroll ke bawah ke bagian "API"
3. Klik "Generate API key" jika Anda belum memilikinya
4. **Salin API key Anda** (dimulai dengan "key...")

### Dapatkan Base ID Anda:
1. Kunjungi [airtable.com/api](https://airtable.com/api)
2. Klik pada base "Database Uni Property" Anda
3. Di URL, Anda akan melihat sesuatu seperti: `https://airtable.com/api/base/appXXXXXXXXXXXXXX`
4. **Salin Base ID** (bagian setelah `/base/` - dimulai dengan "app...")

## ⚙️ Langkah 4: Konfigurasi Website Anda

1. **Buka** `js/airtable-config.js`
2. **Ganti nilai placeholder:**

```javascript
const AIRTABLE_CONFIG = {
    API_KEY: 'keyAPIKeyAndasesungguhnya123', // ← Ganti dengan API key Anda
    BASE_ID: 'appBaseIDAndasesungguhnya456', // ← Ganti dengan Base ID Anda
    TABLE_NAME: 'Properties', // ← Tetap sebagai 'Properties'
    
    // Nama kolom (ubah jika Anda memberi nama kolom yang berbeda)
    COLUMNS: {
        NAME: 'Name',
        LOCATION: 'Location', 
        AREA: 'Area',
        BEDROOMS: 'Bedrooms',
        BATHROOMS: 'Bathrooms',
        PRICE: 'Price',
        IMAGE: 'Image',
        DESCRIPTION: 'Description'
    }
};
```

## 📝 Langkah 5: Tambahkan Data Contoh

Tambahkan beberapa properti contoh untuk menguji integrasi:

### Properti Contoh 1:
- **Name:** Apartemen Modern
- **Location:** Pusat Kota
- **Area:** 120
- **Bedrooms:** 2
- **Bathrooms:** 2
- **Price:** 3500000000
- **Image:** Upload gambar properti

### Properti Contoh 2:
- **Name:** Villa Mewah
- **Location:** Pesisir Pantai
- **Area:** 250
- **Bedrooms:** 4
- **Bathrooms:** 3
- **Price:** 7500000000
- **Image:** Upload gambar properti
- **MapLink:** https://maps.app.goo.gl/xxxxx (Dapatkan dari Google Maps)
- **Sold:** false (unchecked untuk properti yang masih tersedia)

### Properti Contoh 3 (Terjual):
- **Name:** Rumah Keluarga
- **Location:** Perumahan Elite
- **Area:** 180
- **Bedrooms:** 3
- **Bathrooms:** 2
- **Price:** 5000000000
- **Image:** Upload gambar properti
- **MapLink:** https://maps.app.goo.gl/yyyyy
- **Sold:** true (checked untuk properti yang sudah terjual)

## 🚀 Langkah 6: Uji Integrasi Anda

1. **Simpan perubahan** pada `airtable-config.js`
2. **Refresh website Anda**
3. **Periksa console browser** (F12) untuk error apapun
4. **Verifikasi** bahwa properti dimuat dari Airtable

## 🔧 Pemecahan Masalah

### Masalah Umum:

**"Konfigurasi Airtable tidak ditemukan"**
- Pastikan `airtable-config.js` dimuat sebelum `main.js`
- Periksa bahwa nilai konfigurasi Anda benar

**"Gagal mengambil data dari Airtable"**
- Verifikasi API key Anda benar
- Verifikasi Base ID Anda benar
- Periksa koneksi internet Anda

**Gambar tidak muncul**
- Pastikan field "Image" bertipe "Attachment"
- Pastikan gambar telah diupload ke field Attachment

**Harga tidak format dengan benar**
- Masukkan harga sebagai angka (bukan teks)
- Gunakan jumlah penuh (contoh: 3500000000 untuk 3,5 miliar)

## 🗺️ Cara Mendapatkan Link Google Maps

1. **Buka Google Maps** (maps.google.com)
2. **Cari lokasi properti** Anda
3. **Klik "Share" atau "Bagikan"**
4. **Pilih "Copy link"** 
5. **Paste link tersebut** ke kolom MapLink di Airtable

**Contoh link:** `https://maps.app.goo.gl/ABC123xyz`

## 💡 Tips Pro

1. **Gunakan nama gambar yang deskriptif** untuk SEO yang lebih baik
2. **Jaga ukuran gambar tetap wajar** (di bawah 2MB per gambar)
3. **Uji dengan berbagai rentang harga** untuk memverifikasi formatting
4. **Gunakan field Description** untuk detail properti tambahan
5. **Gunakan Google Maps share links** untuk akurasi lokasi yang sempurna
6. **Buat view di Airtable** untuk mengorganisir properti Anda

## 🔒 Catatan Keamanan

**Jangan pernah commit API key Anda ke repository publik!** 
- Jaga `airtable-config.js` tetap privat
- Pertimbangkan menggunakan environment variables untuk produksi

## ✅ Langkah Selanjutnya

Setelah integrasi Airtable Anda berfungsi:

1. **Tambahkan lebih banyak properti** ke base Airtable Anda
2. **Sesuaikan field properti** sesuai kebutuhan
3. **Tambahkan fitur filter/sorting** (opsional)
4. **Siapkan backup otomatis** data Airtable Anda

---

Website Anda sekarang akan secara otomatis menampilkan properti dari database Airtable Anda! 🎉 