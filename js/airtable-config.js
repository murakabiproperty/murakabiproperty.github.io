// Murakabi Property - Airtable Configuration (SECURE VERSION)
// =================================================================================
// ⚠️ KEAMANAN: File ini sekarang menggunakan konfigurasi dari config.js
// JANGAN pernah commit API keys atau tokens ke Git!
// =================================================================================

// Check if secure CONFIG is loaded
if (typeof CONFIG === 'undefined') {
    console.error('🚨 KEAMANAN: File config.js tidak ditemukan!');
    console.error('📖 Baca SECURITY_GUIDE.md untuk setup yang aman.');
    console.error('🔧 Copy js/config.example.js ke js/config.js dan isi dengan credentials real Anda.');
}

const APP_CONFIG = {
    // --- Konfigurasi Airtable (Secure) ---
    AIRTABLE_API_KEY: (typeof CONFIG !== 'undefined' && CONFIG.AIRTABLE) ? CONFIG.AIRTABLE.API_KEY : 'PLACEHOLDER_API_KEY',
    AIRTABLE_BASE_ID: (typeof CONFIG !== 'undefined' && CONFIG.AIRTABLE) ? CONFIG.AIRTABLE.BASE_ID : 'PLACEHOLDER_BASE_ID',
    AIRTABLE_TABLE_NAME: (typeof CONFIG !== 'undefined' && CONFIG.AIRTABLE) ? CONFIG.AIRTABLE.TABLE_NAME : 'Properties',

    // --- Konfigurasi Telegram (Secure) ---
    TELEGRAM_BOT_TOKEN: (typeof CONFIG !== 'undefined' && CONFIG.TELEGRAM) ? CONFIG.TELEGRAM.BOT_TOKEN : 'PLACEHOLDER_BOT_TOKEN',
    TELEGRAM_CHAT_ID: (typeof CONFIG !== 'undefined' && CONFIG.TELEGRAM) ? CONFIG.TELEGRAM.CHAT_ID : 'PLACEHOLDER_CHAT_ID',

    // --- Google Maps API Key (Secure) ---
    GOOGLE_STATIC_MAP_KEY: (typeof CONFIG !== 'undefined' && CONFIG.GOOGLE_MAPS) ? CONFIG.GOOGLE_MAPS.API_KEY : '',

    // --- Pemetaan Kolom Airtable ---
    COLUMNS: (typeof CONFIG !== 'undefined' && CONFIG.AIRTABLE && CONFIG.AIRTABLE.COLUMNS) ? CONFIG.AIRTABLE.COLUMNS : {
        NAME: 'Name',
        LOCATION: 'Location',
        AREA: 'Area',
        AREA_UNIT: 'AreaUnit',
        BEDROOMS: 'Bedrooms',
        BATHROOMS: 'Bathrooms',
        PRICE: 'Price',
        IMAGE: 'Image',
        DESCRIPTION: 'Description',
        MAP_LINK: 'MapLink',
        SOLD: 'Sold'
    }
};

// Security warnings
if (APP_CONFIG.AIRTABLE_API_KEY === 'PLACEHOLDER_API_KEY') {
    console.warn('⚠️ KEAMANAN: Menggunakan placeholder credentials!');
    console.warn('🔧 Setup file config.js dengan credentials real Anda.');
    console.warn('📖 Baca SECURITY_GUIDE.md untuk panduan lengkap.');
}

// Membuat konfigurasi tersedia secara global
window.APP_CONFIG = APP_CONFIG; 