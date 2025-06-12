# 🔧 Debugging: Status "Terjual" Tidak Sync ke Airtable

## Masalah
Ketika status properti diubah ke "Terjual" di aplikasi, checkbox "Sold" di Airtable tidak tercentang.

## Solusi & Debugging

### 1. Pastikan Kolom "Sold" Ada di Airtable
- Buka Airtable Anda
- Pastikan ada kolom bernama **"Sold"** dengan tipe **Checkbox**
- Jika belum ada, tambahkan kolom baru:
  - Nama: `Sold`
  - Tipe: `Checkbox`

### 2. Jalankan Script Test
```bash
cd property-management-app-standalone
python test_status_sync.py
```

Script ini akan:
- ✅ Test koneksi ke Airtable
- ✅ Menampilkan struktur data
- ✅ Test mapping status
- ✅ Update record untuk verifikasi

### 3. Cek Output Aplikasi
Ketika mengupdate status, perhatikan log di console:

**Log yang harus muncul:**
```
🔄 Updating status to 'Terjual' for Airtable record: recXXXXXX
📝 Sending status update to Airtable: status = 'Terjual'
🔄 Status mapping: 'Terjual' -> Sold checkbox: True
📤 Sending to Airtable - Payload: {
  "fields": {
    "Sold": true,
    ...
  }
}
📨 Airtable response status: 200
✅ Successfully updated Airtable record
```

### 4. Kemungkinan Penyebab & Solusi

#### Penyebab 1: Kolom "Sold" Tidak Ada
- **Solusi**: Tambahkan kolom "Sold" dengan tipe Checkbox di Airtable

#### Penyebab 2: Nama Kolom Salah
- **Cek**: Pastikan kolom bernama persis "Sold" (case-sensitive)
- **Solusi**: Update `airtable_config.py` jika nama kolom berbeda

#### Penyebab 3: Tipe Kolom Salah
- **Cek**: Kolom "Sold" harus bertipe Checkbox, bukan Text/Single Select
- **Solusi**: Ubah tipe kolom di Airtable ke Checkbox

#### Penyebab 4: Status Bukan "Terjual"
- **Cek**: Pastikan status di aplikasi persis "Terjual" (dengan huruf besar T)
- **Solusi**: Cek kapitalisasi status

#### Penyebab 5: Koneksi Airtable Bermasalah
- **Cek**: Jalankan `test_status_sync.py` untuk test koneksi
- **Solusi**: Periksa API key dan Base ID

### 5. Manual Test Steps

1. **Buka aplikasi**
2. **Pilih properti**
3. **Klik "Update Status"**
4. **Pilih "Terjual"**
5. **Cek console output**
6. **Refresh Airtable** - checkbox "Sold" harus tercentang

### 6. Verifikasi di Airtable

Setelah update status:
1. Buka Airtable
2. Refresh halaman (Ctrl+R)
3. Cek kolom "Sold" - harus ada centang ✅

### 7. Advanced Debugging

Jika masih bermasalah, cek:

```python
# Di airtable_config.py
COLUMN_MAPPING = {
    'status': 'Sold'  # Pastikan mapping ini benar
}
```

```python
# Di airtable_sync.py, function format_property_for_airtable
if app_field == 'status':
    is_sold = (str(value).lower() == 'terjual')  # Ini harus return True untuk "Terjual"
    print(f"Debug: value='{value}', is_sold={is_sold}")
```

## Debugging Checklist

- [ ] Kolom "Sold" ada di Airtable (tipe Checkbox)
- [ ] Status di aplikasi persis "Terjual"
- [ ] `test_status_sync.py` berhasil
- [ ] Log menunjukkan `Sold: true` di payload
- [ ] Response status 200 dari Airtable
- [ ] Refresh Airtable setelah update

## Kontak Support
Jika masih bermasalah, jalankan `test_status_sync.py` dan kirim output lengkapnya. 