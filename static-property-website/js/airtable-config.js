// Konfigurasi Airtable
// Ganti nilai-nilai ini dengan kredensial Airtable Anda yang sebenarnya

const AIRTABLE_CONFIG = {
    API_KEY: 'pat0cJUQcyOFxDllX.c2421f2ebdfeba1fdf48d662fa60ef05652a4b2deb095f5c5781362aa795c958', // Your Airtable Personal Access Token
    BASE_ID: 'appx1T49Qqh0g3AcF', // Your Airtable Base ID
    TABLE_NAME: 'Properties', // Nama tabel Anda di Airtable
    
    // Nama kolom yang diharapkan di Airtable Anda (Anda dapat menyesuaikan ini)
    COLUMNS: {
        NAME: 'Name',
        LOCATION: 'Location', 
        AREA: 'Area',
        BEDROOMS: 'Bedrooms',
        BATHROOMS: 'Bathrooms',
        PRICE: 'Price',
        IMAGE: 'Image', // Ini harus berupa field attachment
        DESCRIPTION: 'Description', // Opsional
        MAP_LINK: 'MapLink', // Link Google Maps share untuk lokasi properti
        SOLD: 'Sold' // Status terjual (checkbox: true/false)
    }
};

// Ekspor untuk digunakan di main.js
window.AIRTABLE_CONFIG = AIRTABLE_CONFIG; 