// /f%3A/my_property_website/property_website_bagus/js/airtable-config.js

// =================================================================================
// KONFIGURASI PENTING
// =================================================================================
// File ini berisi semua kunci API, ID, dan nama kolom untuk aplikasi.
// Jangan membagikan file ini atau mempublikasikannya secara publik.
// =================================================================================

const APP_CONFIG = {
    // --- Konfigurasi Airtable ---
    // Kunci API Personal Access Token dari akun Airtable Anda.
    AIRTABLE_API_KEY: 'pat0cJUQcyOFxDllX.c2421f2ebdfeba1fdf48d662fa60ef05652a4b2deb095f5c5781362aa795c958', 
    
    // ID dari Airtable Base yang Anda gunakan.
    AIRTABLE_BASE_ID: 'appx1T49Qqh0g3AcF', 
    
    // Nama tabel properti di dalam Base Anda.
    AIRTABLE_TABLE_NAME: 'Properties',

    // --- Konfigurasi Telegram ---
    // Token dari bot Telegram yang Anda buat melalui @BotFather.
    TELEGRAM_BOT_TOKEN: '7633063242:AAHKGy4bb84_nS47v3bN0OQzzT_o0dqCmNo',

    // ID Chat unik untuk tujuan pengiriman notifikasi (bisa grup atau personal).
    TELEGRAM_CHAT_ID: '2142354455',

    // --- (Opsional) Google Static Map API Key ---
    // Isi jika Anda memiliki API key Google Maps Static API untuk preview peta yang lebih stabil.
    // Jika dibiarkan kosong, sistem akan mencoba memuat tanpa key (ber-watermark) dan fallback ke placeholder jika gagal.
    GOOGLE_STATIC_MAP_KEY: '',

    // --- Pemetaan Kolom Airtable ---
    // Sesuaikan nama string di sebelah kanan jika nama kolom di Airtable Anda berbeda.
    COLUMNS: {
        NAME: 'Name',             // Tipe: Single line text
        LOCATION: 'Location',       // Tipe: Single line text
        AREA: 'Area',             // Tipe: Number (integer)
        BEDROOMS: 'Bedrooms',         // Tipe: Number (integer)
        BATHROOMS: 'Bathrooms',       // Tipe: Number (integer)
        PRICE: 'Price',           // Tipe: Number (integer atau currency)
        IMAGE: 'Image',           // Tipe: Attachment (hanya gambar pertama yang akan digunakan)
        DESCRIPTION: 'Description', // Tipe: Rich text atau long text (opsional)
        MAP_LINK: 'MapLink',        // Tipe: URL (opsional)
        SOLD: 'Sold'              // Tipe: Checkbox (true/false)
    }
};

// Membuat konfigurasi tersedia secara global di seluruh aplikasi.
window.APP_CONFIG = APP_CONFIG; 