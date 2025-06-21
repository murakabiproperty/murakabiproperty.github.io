// Murakabi Property - Fallback Data untuk GitHub Pages Demo
// File ini menyediakan data demo ketika API keys tidak tersedia

const FALLBACK_PROPERTIES = [
    {
        id: 'demo-1',
        fields: {
            'Name': 'Villa Modern Murakabi',
            'Location': 'Kemang, Jakarta Selatan',
            'Area': 350,
            'AreaUnit': 'm²',
            'Bedrooms': 4,
            'Bathrooms': 3,
            'Price': 8500000000,
            'Image': [{'url': 'assets/hero-bg.jpg'}],
            'Description': 'Villa mewah dengan desain modern dan fasilitas lengkap',
            'MapLink': 'https://maps.google.com/?q=Kemang+Jakarta+Selatan',
            'Sold': false
        }
    },
    {
        id: 'demo-2',
        fields: {
            'Name': 'Apartemen Premium Murakabi',
            'Location': 'Sudirman, Jakarta Pusat',
            'Area': 180,
            'AreaUnit': 'm²',
            'Bedrooms': 2,
            'Bathrooms': 2,
            'Price': 4200000000,
            'Image': [{'url': 'assets/hero-bg.jpg'}],
            'Description': 'Apartemen premium dengan view kota yang menakjubkan',
            'MapLink': 'https://maps.google.com/?q=Sudirman+Jakarta+Pusat',
            'Sold': false
        }
    },
    {
        id: 'demo-3',
        fields: {
            'Name': 'Rumah Eksklusif Murakabi',
            'Location': 'Pondok Indah, Jakarta Selatan',
            'Area': 280,
            'AreaUnit': 'm²',
            'Bedrooms': 3,
            'Bathrooms': 3,
            'Price': 6800000000,
            'Image': [{'url': 'assets/hero-bg.jpg'}],
            'Description': 'Rumah eksklusif di kawasan elite dengan taman yang asri',
            'MapLink': 'https://maps.google.com/?q=Pondok+Indah+Jakarta+Selatan',
            'Sold': true
        }
    },
    {
        id: 'demo-4',
        fields: {
            'Name': 'Estate Murakabi Premium',
            'Location': 'Sentul, Bogor',
            'Area': 2.5,
            'AreaUnit': 'ha',
            'Bedrooms': 6,
            'Bathrooms': 5,
            'Price': 15000000000,
            'Image': [{'url': 'assets/hero-bg.jpg'}],
            'Description': 'Estate premium dengan lahan luas, cocok untuk investasi besar',
            'MapLink': 'https://maps.google.com/?q=Sentul+Bogor',
            'Sold': false
        }
    }
];

// Function untuk detect apakah menggunakan fallback data
function isUsingFallbackData() {
    return !CONFIG || 
           CONFIG.AIRTABLE.API_KEY === 'PLACEHOLDER_API_KEY' || 
           CONFIG.AIRTABLE.API_KEY.includes('your_') ||
           !CONFIG.AIRTABLE.API_KEY;
}

// Function untuk get properties (fallback atau real)
async function getProperties() {
    if (isUsingFallbackData()) {
        console.warn('🎭 DEMO MODE: Menggunakan data fallback untuk GitHub Pages');
        console.warn('📝 Untuk data real, setup environment variables atau config.js');
        
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 500));
        
        return FALLBACK_PROPERTIES;
    } else {
        // Use real Airtable API
        return await fetchFromAirtable();
    }
}

// Show demo banner jika menggunakan fallback
function showDemoBanner() {
    if (isUsingFallbackData()) {
        const banner = document.createElement('div');
        banner.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: #FFD700;
            color: #343a40;
            text-align: center;
            padding: 10px;
            font-weight: bold;
            z-index: 10000;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        `;
        banner.innerHTML = `
            🎭 DEMO MODE - Data ini hanya untuk demonstrasi | 
            <a href="SECURITY_GUIDE.md" style="color: #343a40; text-decoration: underline;">Setup API Keys</a>
        `;
        document.body.insertBefore(banner, document.body.firstChild);
        
        // Adjust body margin
        document.body.style.marginTop = '50px';
    }
}

// Initialize demo banner on page load
document.addEventListener('DOMContentLoaded', showDemoBanner);

// Export untuk digunakan di app.js
window.FALLBACK_PROPERTIES = FALLBACK_PROPERTIES;
window.getProperties = getProperties;
window.isUsingFallbackData = isUsingFallbackData; 