# Website Murakabi Property

Website properti mewah dan profesional untuk Murakabi Property, telah diperbarui dengan branding dan identitas visual yang konsisten sesuai dengan panduan gaya visual perusahaan.

## 🎨 **Identitas Visual Murakabi Property**

Website ini telah mengikuti **Panduan Gaya Visual Murakabi Property** dengan filosofi desain:
- **Modern** - Teknologi web terkini dengan desain kontemporer
- **Profesional** - Layout yang bersih dan terorganisir dengan baik
- **Mewah** - Pemilihan warna emas dan tipografi premium
- **Terpercaya** - Interface yang konsisten dan pengalaman pengguna yang handal

### 🎨 Palet Warna
Sesuai dengan style guide Murakabi Property:
- **Warna Primer**: 
  - Putih Bersih (#FFFFFF)
  - Abu-abu Arang (#343a40)
- **Warna Aksen**: 
  - Emas (#FFD700) - Untuk CTA dan elemen penting
- **Warna Sekunder**: 
  - Abu-abu Sangat Terang (#F8F9FA)
  - Emas Tekstual (#D4AF37)
  - Abu-abu Netral (#6c757d)

### ✍️ Tipografi
Font utama: **Inter** dengan hierarki yang jelas:
- **H1**: 800 weight, 60px (3.75rem)
- **H2**: 700 weight, 36px (2.25rem)
- **H3**: 700 weight, 20px (1.25rem)
- **Body**: 400 weight, 16px dengan line-height 1.6

## 🚀 **Fitur Utama Website**

### 1. 🏠 Hero Section
- Background image modern house dengan gradient overlay
- Teks putih untuk kontras optimal
- Judul dengan highlight emas
- CTA button dengan warna emas yang menonjol
- Statistik perusahaan yang menawan

### 2. 🔍 Search & Filter
- Filter properti berdasarkan lokasi, harga, kamar
- Background abu-abu terang untuk kontras
- Interface yang user-friendly

### 3. 🏘️ Listing Properti
- Grid responsif untuk menampilkan properti
- Kartu properti dengan efek hover yang elegant
- Kategori properti yang jelas (Premium, Eksklusif)
- Harga dengan tipografi yang menonjol

### 4. 🛠️ Layanan Premium
- 4 kategori layanan utama
- Ikon dengan background gradient emas
- Deskripsi layanan yang fokus pada kemewahan

### 5. ℹ️ Tentang Murakabi Property
- Cerita perusahaan yang profesional
- Feature highlights dengan ikon emas
- Layout dua kolom yang seimbang

### 6. 📞 Kontak & Modal
- Form kontak yang mudah digunakan
- Modal detail properti dengan peta interaktif
- Informasi kontak lengkap

### 7. 📱 Mobile Responsive
- Design mobile-first
- Navigation yang optimal di semua perangkat
- Breakpoint yang konsisten

### 🏠 Tampilan Properti Dinamis
- **Listing properti** yang diambil langsung dari database Airtable
- **Gambar properti** dengan lazy loading dan fallback
- **Filter properti** berdasarkan lokasi, harga, kamar tidur, dan kamar mandi
- **Modal detail** dengan informasi properti lengkap
- **Peta lokasi** terintegrasi dengan Google Maps

### 📏 Satuan Area Otomatis (BARU!)
- **Tampilan satuan area** otomatis sesuai data dari Airtable
- **Dukungan m² dan hektare (ha)** berdasarkan input di aplikasi
- **Auto-deteksi unit** untuk data lama tanpa informasi satuan
- **Edit unit area** untuk properti yang sudah ada di aplikasi
- **Tidak ada kontrol manual** - professional dan clean
- **Sinkronisasi penuh** dengan aplikasi property management

### 📱 Responsif dan Modern
- **Design responsif** untuk semua device
- **Animasi smooth** dan transisi modern
- **Loading states** yang informatif
- **Error handling** yang baik

### 🔗 Integrasi Airtable
- **Real-time data** dari Airtable
- **Fallback data** untuk mode demo
- **Automatic sync** dengan aplikasi management

## 📁 **Struktur File**

```
property_website_bagus/
├── index.html              # Halaman utama dengan branding Murakabi Property
├── styles.css              # Stylesheet lengkap dengan palet warna sesuai style guide
├── js/
│   ├── airtable-config.js   # Konfigurasi database Airtable
│   └── app.js               # JavaScript utama untuk interaksi
├── assets/
│   ├── logo.png             # Logo Murakabi Property
│   └── favicon.png          # Favicon website
└── README.md                # Dokumentasi ini
```

## ⚙️ **Setup & Konfigurasi**

### 🔐 **KEAMANAN PENTING**
**JANGAN pernah commit API keys, bot tokens, atau informasi sensitif ke Git!**

Baca panduan lengkap: [`SECURITY_GUIDE.md`](SECURITY_GUIDE.md)

### 1. Setup Konfigurasi Aman
```bash
# 1. Copy example configuration
cp js/config.example.js js/config.js

# 2. Edit dengan credentials real Anda
nano js/config.js

# 3. Pastikan .gitignore aktif (config.js tidak boleh ter-commit)
git status
```

### 2. Database Airtable
Website terintegrasi dengan Airtable untuk manajemen data properti.

**Setup Aman:**
```javascript
// js/config.js (JANGAN commit file ini)
const CONFIG = {
    AIRTABLE: {
        API_KEY: 'pat_your_real_airtable_token_here',
        BASE_ID: 'your_real_base_id_here',
        TABLE_NAME: 'Properties',
        COLUMNS: {
            NAME: 'Name',
            LOCATION: 'Location',
            AREA: 'Area',
            BEDROOMS: 'Bedrooms',
            BATHROOMS: 'Bathrooms',
            PRICE: 'Price',
            IMAGE: 'Image',
            MAP_LINK: 'MapLink',
            SOLD: 'Sold'
        }
    }
};
```

### 3. Deployment Aman
Website ini adalah static website yang bisa di-deploy ke:

#### **Netlify (Recommended)**
```bash
# 1. Deploy ke Netlify
# 2. Set environment variables di dashboard:
#    Site settings > Environment variables
AIRTABLE_API_KEY=your_real_key_here
TELEGRAM_BOT_TOKEN=your_real_token_here
```

#### **Vercel**
```bash
# Set environment variables
vercel env add AIRTABLE_API_KEY
vercel env add TELEGRAM_BOT_TOKEN
```

#### **GitHub Pages + Actions**
```yaml
# .github/workflows/deploy.yml
env:
  AIRTABLE_API_KEY: ${{ secrets.AIRTABLE_API_KEY }}
```

#### **GitHub Pages**
```bash
# Simple demo deployment
git push origin main
# Enable GitHub Pages di repository settings

# Production dengan real data
# Setup GitHub Secrets, lalu push
```
📖 **Panduan lengkap**: [`GITHUB_PAGES_GUIDE.md`](GITHUB_PAGES_GUIDE.md)

#### **Traditional Web Hosting**
- Upload files via FTP
- Gunakan server-side proxy untuk API calls
- Atau gunakan EmailJS/Formspree untuk contact forms

### 3. Custom Domain (Opsional)
Untuk branding yang lebih profesional, gunakan domain custom seperti:
- `www.murakabiproperty.com`
- `www.murakabiproperty.co.id`

## 🎯 **Komponen UI Sesuai Style Guide**

### Buttons
- **Primary Button**: 
  - Background: Emas (#FFD700)
  - Text: Abu-abu Arang (#343a40)
  - Font-weight: 700
  - Hover effect: Slight darkening dengan transform

- **Secondary Button**: 
  - Background: Abu-abu Arang (#343a40)
  - Text: Putih (#FFFFFF)
  - Font-weight: 700
  - Hover effect: Lighter shade

### Cards
- **Property Cards**:
  - Background: Putih (#FFFFFF)
  - Border radius: 12px
  - Shadow: Subtle dengan efek hover
  - Border: Light gray (#e9ecef)

### Forms
- **Input Fields**:
  - Border focus: Emas (#FFD700)
  - Font: Inter Medium untuk labels
  - Placeholder: Abu-abu Netral

## 📊 **Performance & SEO**

- ✅ **Fast Loading**: Minimal JavaScript, optimized CSS
- ✅ **SEO Friendly**: Semantic HTML, proper meta tags
- ✅ **Accessible**: ARIA labels, keyboard navigation
- ✅ **Mobile Optimized**: Responsive design
- ✅ **Modern Browser Support**: CSS variables, modern JS

## 🎨 **Customization**

Untuk mengubah warna atau branding, edit CSS variables di `styles.css`:

```css
:root {
  /* Murakabi Property Color Palette */
  --primary-color: #FFD700;        /* Emas */
  --secondary-color: #343a40;      /* Abu-abu Arang */
  --accent-color: #D4AF37;         /* Emas Tekstual */
  --white: #FFFFFF;                /* Putih Bersih */
  --light-bg: #F8F9FA;            /* Abu-abu Sangat Terang */
  --gray-text: #6c757d;           /* Abu-abu Netral */
}
```

## 🔄 **Updates dari Versi Sebelumnya**

### ✨ Branding Updates
- ✅ Nama perusahaan: "Uni Property" → "Murakabi Property"
- ✅ Tagline: "Solusi Properti Mewah & Terpercaya"
- ✅ Logo: Diganti dengan logo Murakabi Property
- ✅ Color scheme: Orange → Gold/Charcoal sesuai style guide

### 🎨 Design Updates (Light Theme)
- ✅ **Overall Theme**: Dark theme → Clean light theme
- ✅ **Navigation**: Dark background → White with charcoal text + brand text
- ✅ **Typography**: Playfair Display → Inter (sesuai style guide)
- ✅ **Hero background**: Modern house image dengan gradient overlay + white text
- ✅ **Button colors**: Orange → Gold primary, charcoal secondary
- ✅ **Section backgrounds**: Consistent white/very light gray alternating
- ✅ **Property cards**: Dark theme → White background dengan subtle shadows
- ✅ **Service cards**: Dark → White cards dengan gold accents
- ✅ **Forms**: Dark inputs → Clean white form fields
- ✅ **About section**: Dark background → Light background
- ✅ **Contact section**: Gray → White background

### 📝 Content Updates
- ✅ Hero subtitle: Focus pada kemewahan dan investasi
- ✅ Services: Emphasis pada "Premium", "Eksklusif", "Mewah"
- ✅ About section: Cerita Murakabi Property yang baru
- ✅ Contact info: Email domain disesuaikan

## 🎯 **Target Audience**

Website ini dirancang untuk:
- 🏢 **Investor Properti** - Yang mencari ROI tinggi
- 💰 **High-Net-Worth Individuals** - Yang menginginkan properti mewah
- 🏠 **Homebuyers Premium** - Yang mencari kualitas terbaik
- 🏢 **Corporate Clients** - Yang membutuhkan properti bisnis eksklusif

## 📞 **Support & Maintenance**

Untuk dukungan teknis atau updates website:
- 📧 Email: info@murakabiproperty.co.id
- 📱 Phone: 08115221998
- 🏢 Alamat: Jl. Pramuka, Perumahan Akasia Permai Blok C No 12, Pasir Panjang, Arut Selatan, Pangkalan Bun, Kotawaringin Barat

---

## 📜 **License & Copyright**

© 2024 Murakabi Property. Solusi Properti Mewah & Terpercaya.
All Rights Reserved.

---

**🎨 Designed with Murakabi Property Style Guide**  
**💻 Developed with Modern Web Technologies**  
**🚀 Optimized for Performance & User Experience** 