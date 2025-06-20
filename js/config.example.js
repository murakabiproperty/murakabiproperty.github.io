// Murakabi Property - Configuration Example
// Copy this file to config.js and fill with your actual values
// NEVER commit config.js with real credentials to version control

const CONFIG = {
    // Airtable Configuration
    AIRTABLE: {
        API_KEY: 'your_airtable_personal_access_token_here',
        BASE_ID: 'your_airtable_base_id_here',
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

    // Telegram Bot (if using for notifications)
    TELEGRAM: {
        BOT_TOKEN: 'your_telegram_bot_token_here',
        CHAT_ID: 'your_telegram_chat_id_here'
    },

    // Google Maps (if using)
    GOOGLE_MAPS: {
        API_KEY: 'your_google_maps_api_key_here'
    },

    // Development/Production flags
    ENVIRONMENT: 'development', // 'development' or 'production'
    DEBUG: true
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
} else {
    window.CONFIG = CONFIG;
} 