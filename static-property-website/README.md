# Website Murakabi Property

Website properti modern dan mewah untuk Murakabi Property, dibangun mengikuti panduan gaya visual yang profesional dan elegan.

## 🎨 Desain & Branding

Website ini mengikuti **Panduan Gaya Visual Murakabi Property** dengan filosofi desain:
- **Modern** - Menggunakan teknologi web terkini
- **Profesional** - Layout yang bersih dan terorganisir
- **Mewah** - Pemilihan warna dan tipografi premium
- **Terpercaya** - Interface yang konsisten dan mudah digunakan

### Palet Warna
- **Warna Primer**: Putih (#FFFFFF), Abu-abu Arang (#343a40)
- **Warna Aksen**: Emas (#FFD700)
- **Warna Sekunder**: Abu-abu Sangat Terang (#F8F9FA), Emas Tekstual (#D4AF37), Abu-abu Netral (#6c757d)

### Tipografi
Font utama: **Inter** (400, 500, 600, 700, 800)
- Hierarki teks yang jelas dari H1 hingga body text
- Keterbacaan optimal di semua perangkat

## 🚀 Fitur Utama

### 1. Hero Section
- Sambutan yang menarik dengan branding Murakabi Property
- Call-to-Action yang menonjol

### 2. Listing Properti
- Kartu properti dengan desain modern
- Kategori properti (APARTEMEN, VILLA, RUMAH)
- Informasi lengkap: lokasi, luas, kamar, harga
- Efek hover yang elegant

### 3. Modal Kontak
- Form kontak untuk inquiries
- Integrasi Google Maps untuk lokasi
- Validasi form yang user-friendly

### 4. Responsif
- Mobile-first design
- Navigasi bawah untuk mobile
- Optimized untuk semua ukuran layar

### 5. Integrasi Airtable
- Data properti dinamis dari Airtable
- Real-time updates
- Status "Terjual" otomatis

## 📁 Struktur File

```
static-property-website/
├── assets/
│   └── logo.png              # Logo Murakabi Property
├── css/
│   └── styles.css            # Stylesheet utama dengan variabel CSS
├── js/
│   ├── airtable-config.js    # Konfigurasi Airtable
│   └── main.js               # JavaScript utama
├── index.html                # Halaman utama
└── README.md                 # Dokumentasi ini
```

## ⚙️ Setup & Konfigurasi

### 1. Airtable Setup
Edit file `js/airtable-config.js`:
```javascript
const AIRTABLE_CONFIG = {
    API_KEY: 'your_airtable_api_key',
    BASE_ID: 'your_base_id',
    TABLE_NAME: 'Properties',
    // ... kolom lainnya
};
```

### 2. Telegram Bot (Opsional)
Edit file `js/main.js` untuk notifikasi:
```javascript
const TELEGRAM_BOT_TOKEN = 'your_bot_token';
const TELEGRAM_CHAT_ID = 'your_chat_id';
```

### 3. Deployment
Website ini adalah static website yang bisa di-deploy ke:
- GitHub Pages
- Netlify
- Vercel
- Web hosting tradisional

## 🎯 Komponen UI

### Buttons
- **Primary Button**: Background emas (#FFD700), teks abu-abu arang
- **Secondary Button**: Background abu-abu arang, teks putih

### Cards
- Border radius: 12px
- Shadow yang halus dengan efek hover
- Transisi smooth untuk semua interaksi

### Forms
- Border focus dengan warna emas
- Label yang jelas dengan font Inter Medium
- Validasi visual

### Loading States
- Spinner dengan warna branding
- Error states dengan pesan yang jelas

## 📱 Responsive Breakpoints

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px  
- **Desktop**: > 1024px

## 🔧 Teknologi

- **HTML5** - Struktur semantic
- **CSS3** - Custom properties, Flexbox, Grid
- **Vanilla JavaScript** - Tanpa framework untuk performa optimal
- **Tailwind CSS** - Utility-first CSS framework
- **Inter Font** - Typography modern via Google Fonts

## 📊 Performance

- Optimized images
- Minimal JavaScript
- CSS variables untuk konsistensi
- Lazy loading untuk gambar properti

## 🎨 Customization

Untuk mengubah branding, edit variabel CSS di `css/styles.css`:

```css
:root {
    --color-putih: #FFFFFF;
    --color-arang: #343a40;
    --color-emas: #FFD700;
    /* ... variabel lainnya */
}
```

## 📞 Support

Untuk dukungan teknis atau pertanyaan mengenai website ini, silakan hubungi tim pengembang.

---

© 2024 Murakabi Property. Solusi Properti Mewah & Terpercaya. 