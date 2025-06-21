// Murakabi Property - Configuration
// Copy this file to config.js and fill with your actual values
// NEVER commit config.js with real credentials to version control

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
            MAP_LINK: 'MapLink',
            SOLD: 'Sold'
        }
    },

    // Contact Form Configuration
    CONTACT: {
        // Option 1: EmailJS (Recommended for static sites)
        EMAILJS: {
            SERVICE_ID: 'your_emailjs_service_id',
            TEMPLATE_ID: 'your_emailjs_template_id',
            PUBLIC_KEY: 'your_emailjs_public_key'
        },
        
        // Option 2: Formspree (Alternative)
        FORMSPREE: {
            ENDPOINT: 'https://formspree.io/f/your_form_id'
        },

        // Option 3: Netlify Forms (if hosted on Netlify)
        NETLIFY_FORMS: true
    },

    // Telegram Bot (Updated with new credentials)
    TELEGRAM: {
        BOT_TOKEN: '7554674052:AAEpEAx-sChhjwiLVIUlmqhbUlT46beyhew',
        CHAT_ID: '908233061'
    },

    // Google Maps (if using)
    GOOGLE_MAPS: {
        API_KEY: 'your_google_maps_api_key_here'
    },

    // Development/Production flags
    ENVIRONMENT: 'production', // 'development' or 'production'
    DEBUG: false
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
} else {
    window.CONFIG = CONFIG;
} 
