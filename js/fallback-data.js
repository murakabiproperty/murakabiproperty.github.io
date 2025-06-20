// Murakabi Property - Fallback Data untuk GitHub Pages Demo
// File ini menyediakan data demo ketika API keys tidak tersedia

const FALLBACK_PROPERTIES = [
    {
        id: 'demo-1',
        name: 'Villa Modern Murakabi',
        location: 'Kemang, Jakarta Selatan',
        area: 350,
        bedrooms: 4,
        bathrooms: 3,
        price: 8500000000,
        image: 'assets/hero-bg.jpg',
        description: 'Villa mewah dengan desain modern dan fasilitas lengkap',
        mapLink: 'https://maps.google.com/?q=Kemang+Jakarta+Selatan',
        sold: false,
        featured: true
    },
    {
        id: 'demo-2',
        name: 'Apartemen Premium Murakabi',
        location: 'Sudirman, Jakarta Pusat',
        area: 180,
        bedrooms: 2,
        bathrooms: 2,
        price: 4200000000,
        image: 'assets/hero-bg.jpg',
        description: 'Apartemen premium dengan view kota yang menakjubkan',
        mapLink: 'https://maps.google.com/?q=Sudirman+Jakarta+Pusat',
        sold: false,
        featured: false
    },
    {
        id: 'demo-3',
        name: 'Rumah Eksklusif Murakabi',
        location: 'Pondok Indah, Jakarta Selatan',
        area: 280,
        bedrooms: 3,
        bathrooms: 3,
        price: 6800000000,
        image: 'assets/hero-bg.jpg',
        description: 'Rumah eksklusif di kawasan elite dengan taman yang asri',
        mapLink: 'https://maps.google.com/?q=Pondok+Indah+Jakarta+Selatan',
        sold: true,
        featured: false
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
        
        return {
            success: true,
            data: FALLBACK_PROPERTIES,
            message: 'Demo data loaded successfully'
        };
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