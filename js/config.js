// Murakabi Property - Configuration (REAL DATA VERSION)
// =================================================================================
// 🚀 PRODUCTION MODE: File ini menggunakan real credentials untuk data real
// Data akan diambil langsung dari Airtable
// =================================================================================

const CONFIG = {
    // Airtable Configuration
    AIRTABLE: {
        API_KEY: 'pat0cJUQcyOFxDllX.c2421f2ebdfeba1fdf48d662fa60ef05652a4b2deb095f5c5781362aa795c958',
        BASE_ID: 'appx1T49Qqh0g3AcF',
        TABLE_NAME: 'Properties',
        COLUMNS: {
            NAME: 'Name',
            LOCATION: 'Location',
            AREA: 'Area',
            BEDROOMS: 'Bedrooms',
            BATHROOMS: 'Bathrooms',
            PRICE: 'Price',
            IMAGE: 'Image',
            DESCRIPTION: 'Description',
            MAP_LINK: 'MapLink',
            SOLD: 'Sold'
        }
    },

    // Telegram Bot Configuration
    TELEGRAM: {
        BOT_TOKEN: '7554674052:AAEpEAx-sChhjwiLVIUlmqhbUlT46beyhew',
        CHAT_ID: '908233061'
    },

    // Contact Form Configuration
    CONTACT: {
        // EmailJS (Recommended for static sites)
        EMAILJS: {
            SERVICE_ID: 'your_emailjs_service_id',
            TEMPLATE_ID: 'your_emailjs_template_id',
            PUBLIC_KEY: 'your_emailjs_public_key'
        },
        
        // Formspree (Alternative)
        FORMSPREE: {
            ENDPOINT: 'https://formspree.io/f/your_form_id'
        }
    },

    // Google Maps (Optional)
    GOOGLE_MAPS: {
        API_KEY: ''
    },

    // Environment
    ENVIRONMENT: 'production',
    DEBUG: false
};

// Make CONFIG available globally
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
} else {
    window.CONFIG = CONFIG;
} 
