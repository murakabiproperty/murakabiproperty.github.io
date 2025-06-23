// --- Start of Logic Integration ---
// Fungsi API Airtable
async function fetchPropertiesFromAirtable() {
    const config = window.APP_CONFIG;
    if (!config || !config.AIRTABLE_API_KEY || !config.AIRTABLE_BASE_ID) {
        throw new Error('Konfigurasi Airtable tidak ditemukan atau tidak lengkap');
    }
    
    const url = `https://api.airtable.com/v0/${config.AIRTABLE_BASE_ID}/${config.AIRTABLE_TABLE_NAME}`;
    console.log('🔍 Mencoba mengakses Airtable:', url);
    
    try {
        const response = await fetch(url, {
            headers: {
                'Authorization': `Bearer ${config.AIRTABLE_API_KEY}`,
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error('❌ Airtable Error Response:', errorText);
            throw new Error(`Airtable API Error: ${response.status} - ${errorText}`);
        }

        const data = await response.json();
        console.log('✅ Data berhasil dimuat:', data.records?.length, 'properti');
        return data.records;
    } catch (error) {
        console.error('💥 Error saat mengambil properti dari Airtable:', error);
        throw error;
    }
}

function showLoadingState() {
    const propertiesContainer = document.querySelector('.properties-grid');
    if (!propertiesContainer) return;

    propertiesContainer.innerHTML = `
        <div class="col-span-full flex justify-center items-center py-12">
            <div class="text-center">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500 mx-auto mb-4"></div>
                <p class="text-gray-600">Memuat properti...</p>
            </div>
        </div>
    `;
}

let allProperties = []; // Store all properties globally
let currentPropertyIndex = 0;
let propertiesPerPage = 6;

// Area display function - reads unit from data
function formatAreaDisplay(area, unit) {
    if (!area || area === 'N/A') return 'N/A';
    
    const numArea = parseFloat(area);
    if (isNaN(numArea)) return 'N/A';
    
    // Helper function to remove unnecessary .00
    function formatNumber(num) {
        return num % 1 === 0 ? num.toString() : num.toFixed(2).replace(/\.?0+$/, '');
    }
    
    // Normalize unit variations
    let normalizedUnit = unit ? unit.toLowerCase().trim() : '';
    
    // Handle different unit formats
    if (normalizedUnit === 'hektare' || normalizedUnit === 'hectare' || normalizedUnit === 'ha') {
        // Area is already in hectares
        return `${formatNumber(numArea)} ha`;
    } else if (normalizedUnit === 'm²' || normalizedUnit === 'm2' || normalizedUnit === 'meter persegi') {
        // Area is in square meters
        if (numArea >= 10000) {
            // Convert large m² to hectares for better readability
            const hectares = numArea / 10000;
            return `${formatNumber(hectares)} ha`;
        } else {
            return `${formatNumber(numArea)} m²`;
        }
    } else if (!unit || unit === '') {
        // Auto-detect best unit if not specified
        if (numArea >= 10000) {
            const hectares = numArea / 10000;
            return `${formatNumber(hectares)} ha`;
        } else {
            return `${formatNumber(numArea)} m²`;
        }
    }
    
    // Default fallback
    return `${formatNumber(numArea)} ${unit || 'm²'}`;
}

function getPropertiesPerPage() {
    return window.innerWidth <= 768 ? 3 : 6;
}

function renderProperties(properties, reset = false) {
    const propertiesContainer = document.querySelector('.properties-grid');
    if (!propertiesContainer) return;

    if (reset) {
        propertiesContainer.innerHTML = '';
        currentPropertyIndex = 0;
        propertiesPerPage = getPropertiesPerPage();
    }

    if (properties.length === 0) {
        propertiesContainer.innerHTML = `<div class="col-span-full text-center py-12"><p class="text-gray-600">Tidak ada properti yang tersedia saat ini.</p></div>`;
        // Hapus tombol load more jika ada
        let loadMoreBtn = document.getElementById('load-more-properties');
        if (loadMoreBtn) loadMoreBtn.remove();
        return;
    }

    // Tentukan properti yang akan ditampilkan
    const nextIndex = currentPropertyIndex + propertiesPerPage;
    const propertiesToShow = properties.slice(currentPropertyIndex, nextIndex);

    propertiesToShow.forEach(property => {
        const fields = property.fields;
        const propertyCard = createPropertyCard(fields);
        propertiesContainer.appendChild(propertyCard);
    });

    currentPropertyIndex += propertiesToShow.length;

    // Tambahkan/hapus tombol 'Lihat Lebih Banyak'
    let loadMoreBtn = document.getElementById('load-more-properties');
    if (loadMoreBtn) loadMoreBtn.remove();

    if (currentPropertyIndex < properties.length) {
        loadMoreBtn = document.createElement('button');
        loadMoreBtn.id = 'load-more-properties';
        loadMoreBtn.className = 'btn btn-outline';
        loadMoreBtn.innerHTML = 'Lihat Lebih Banyak <i class="fas fa-arrow-down"></i>';
        loadMoreBtn.style.margin = '2rem auto 0';
        loadMoreBtn.style.display = 'block';
        loadMoreBtn.onclick = function() {
            renderProperties(properties);
        };
        propertiesContainer.parentNode.appendChild(loadMoreBtn);
    }
}

function createPropertyCard(fields) {
    const config = window.APP_CONFIG;
    const cols = config ? config.COLUMNS : {};
    
    const name = fields[cols.NAME] || 'Properti Tanpa Nama';
    const location = fields[cols.LOCATION] || 'Tidak ditentukan';
    const area = fields[cols.AREA] || 'N/A';
    const areaUnit = fields[cols.AREA_UNIT] || 'm²';
    
    // Debug logging untuk area dan unit
    console.log(`🏠 ${name}:`, {
        area: area,
        areaUnit: areaUnit,
        rawAreaData: fields[cols.AREA],
        rawUnitData: fields[cols.AREA_UNIT],
        allFields: fields
    });
    const bedrooms = fields[cols.BEDROOMS] || 'N/A';
    const bathrooms = fields[cols.BATHROOMS] || 'N/A';
    const price = fields[cols.PRICE];
    const imageField = fields[cols.IMAGE];
    const isSold = fields[cols.SOLD] || false;
    
    const card = document.createElement('div');
    card.className = `property-card ${isSold ? 'sold' : ''}`;
    card.setAttribute('data-area', area);
    card.setAttribute('data-bedrooms', bedrooms);
    card.setAttribute('data-bathrooms', bathrooms);

    const imageUrl = imageField && imageField.length > 0 
        ? imageField[0].url 
        : 'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400&h=300&fit=crop';
    
    const formattedPrice = formatPrice(price);
    
    card.innerHTML = `
        <div class="property-image">
            <img src="${imageUrl}" alt="${name}">
            ${!isSold 
                ? '<div class="property-badge">Terbaru</div>' 
                : '<div class="property-badge sold">TERJUAL</div>'}
            <div class="property-overlay">
                ${!isSold ? '<button class="btn btn-white">Lihat Detail</button>' : ''}
            </div>
        </div>
        <div class="property-content">
            <div class="property-price">${formattedPrice}</div>
            <h3 class="property-title">${name}</h3>
            <p class="property-location">
                <i class="fas fa-map-marker-alt"></i>
                ${location}
            </p>
            <div class="property-area">
                <i class="fas fa-expand-arrows-alt"></i>
                ${formatAreaDisplay(area, areaUnit)}
            </div>
            <div class="property-features">
                <span class="feature">
                    <i class="fas fa-bed"></i>
                    ${bedrooms} Kamar
                </span>
                <span class="feature">
                    <i class="fas fa-bath"></i>
                    ${bathrooms} Kamar Mandi
                </span>
            </div>
        </div>
    `;
    
    // Disable click for sold property
    if (isSold) {
        card.style.pointerEvents = 'none';
        card.style.opacity = '0.6';
    } else {
        const detailBtn = card.querySelector('.btn-white');
        if (detailBtn) {
            detailBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                showPropertyModal(fields);
            });
        }
    }

    return card;
}

function formatPrice(price) {
    if (!price) return 'Harga tidak tersedia';
    
    if (price >= 1000000000) {
        return `Rp ${(price / 1000000000).toFixed(1)} Miliar`;
    } else if (price >= 1000000) {
        return `Rp ${(price / 1000000).toFixed(0)} Juta`;
    } else {
        return `Rp ${price.toLocaleString('id-ID')}`;
    }
}

function openGoogleMaps(location, propertyName) {
    if (!location || location === 'Tidak ditentukan') {
        alert('Lokasi tidak tersedia untuk properti ini.');
        return;
    }
    const query = encodeURIComponent(`${location}, Indonesia`);
    const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${query}`;
    window.open(mapsUrl, '_blank');
}

async function showPropertyModal(fields) {
    const config = window.APP_CONFIG;
    const cols = config.COLUMNS;

    const titleEl = document.getElementById("modal-property-title");
    const locationEl = document.getElementById("modal-property-location");
    const priceEl = document.getElementById("modal-property-price");
    const areaEl = document.getElementById("modal-property-area");
    const bedEl = document.getElementById("modal-property-bedrooms");
    const bathEl = document.getElementById("modal-property-bathrooms");
    const mapImg = document.getElementById("modal-map-image");
    const mapLink = document.getElementById("modal-map-link");

    const name = fields[cols.NAME] || "Properti";
    const location = fields[cols.LOCATION] || "-";
    const area = formatAreaDisplay(fields[cols.AREA], fields[cols.AREA_UNIT]) || "-";
    
    // Debug modal data
    console.log(`📋 Modal ${name}:`, {
        area: fields[cols.AREA],
        unit: fields[cols.AREA_UNIT],
        formatted: area
    });
    const bedrooms = fields[cols.BEDROOMS] ? `${fields[cols.BEDROOMS]} Kamar` : "-";
    const bathrooms = fields[cols.BATHROOMS] ? `${fields[cols.BATHROOMS]} Kamar Mandi` : "-";
    const price = formatPrice(fields[cols.PRICE]);

    if(titleEl) titleEl.textContent = name;
    if(locationEl) locationEl.textContent = location;
    if(priceEl) priceEl.textContent = price;
    if(areaEl) areaEl.textContent = area;
    if(bedEl) bedEl.textContent = bedrooms;
    if(bathEl) bathEl.textContent = bathrooms;

    // Map handling (static preview)
    if (mapImg && mapLink) {
        const placeholderMap = 'assets/map-placeholder.png'; // local static map image
        mapImg.src = placeholderMap;
        mapLink.href = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(location)}`;

        // ensure fallback if image fails to load
        if (mapImg) {
            mapImg.onerror = function() {
                this.onerror = null;
                this.src = 'https://images.unsplash.com/photo-1502920917128-1aa500764b84?w=500&h=200&fit=crop';
            };
        }

        if (mapImg) {
            mapImg.classList.add('no-filter');
        }
    }

    const modalOverlay = document.getElementById("property-modal-overlay");
    if(modalOverlay){
        modalOverlay.classList.add("active");
        document.body.style.overflow='hidden';
    }
}

// --- Start of Filter Logic ---

// Test function to populate filters with dummy data
function testPopulateFilters() {
    console.log('🧪 Testing filter population with dummy data');
    
    const locationFilter = document.getElementById('filter-location');
    const priceFilter = document.getElementById('filter-price');
    const bedroomsFilter = document.getElementById('filter-bedrooms');
    const bathroomsFilter = document.getElementById('filter-bathrooms');
    
    console.log('🧪 Filter elements:', {
        location: !!locationFilter,
        price: !!priceFilter,
        bedrooms: !!bedroomsFilter,
        bathrooms: !!bathroomsFilter
    });
    
    if (locationFilter) {
        // Add dummy locations
        ['Jakarta', 'Bandung', 'Surabaya'].forEach(location => {
            const option = document.createElement('option');
            option.value = location;
            option.textContent = location;
            locationFilter.appendChild(option);
        });
        console.log('✅ Dummy locations added');
    }
    
    if (bedroomsFilter) {
        // Add dummy bedrooms
        [1, 2, 3, 4, 5].forEach(num => {
            const option = document.createElement('option');
            option.value = num;
            option.textContent = `${num} Kamar`;
            bedroomsFilter.appendChild(option);
        });
        console.log('✅ Dummy bedrooms added');
    }
    
    if (bathroomsFilter) {
        // Add dummy bathrooms
        [1, 2, 3, 4].forEach(num => {
            const option = document.createElement('option');
            option.value = num;
            option.textContent = `${num} Kamar Mandi`;
            bathroomsFilter.appendChild(option);
        });
        console.log('✅ Dummy bathrooms added');
    }
    
    if (priceFilter) {
        // Add dummy price ranges
        const priceRanges = [
            { label: '< 500 Juta', value: '0-499999999' },
            { label: '500 Juta - 1 M', value: '500000000-1000000000' },
            { label: '1 M - 2 M', value: '1000000001-2000000000' },
            { label: '> 2 M', value: '2000000001-Infinity' },
        ];
        
        priceRanges.forEach(range => {
            const option = document.createElement('option');
            option.value = range.value;
            option.textContent = range.label;
            priceFilter.appendChild(option);
        });
        console.log('✅ Dummy price ranges added');
    }
}

function populateFilters(properties) {
    console.log('🔧 Populating filters with', properties.length, 'properties');
    console.log('🔧 APP_CONFIG:', window.APP_CONFIG);
    
    const locationFilter = document.getElementById('filter-location');
    const priceFilter = document.getElementById('filter-price');
    const bedroomsFilter = document.getElementById('filter-bedrooms');
    const bathroomsFilter = document.getElementById('filter-bathrooms');
    
    if (!locationFilter || !priceFilter || !bedroomsFilter || !bathroomsFilter) {
        console.error('❌ Filter elements not found');
        return;
    }
    
    const config = window.APP_CONFIG;
    if (!config || !config.COLUMNS) {
        console.error('❌ APP_CONFIG or COLUMNS not found');
        return;
    }
    
    const locations = [...new Set(properties.map(p => p.fields[config.COLUMNS.LOCATION]).filter(Boolean))];
    const bedrooms = [...new Set(properties.map(p => p.fields[config.COLUMNS.BEDROOMS]).filter(Boolean).sort((a,b) => a-b))];
    const bathrooms = [...new Set(properties.map(p => p.fields[config.COLUMNS.BATHROOMS]).filter(Boolean).sort((a,b) => a-b))];

    console.log('🔧 Extracted data:', { locations, bedrooms, bathrooms });

    // Clear existing options (except the first default option)
    locationFilter.innerHTML = '<option value="">Semua Lokasi</option>';
    bedroomsFilter.innerHTML = '<option value="">Semua</option>';
    bathroomsFilter.innerHTML = '<option value="">Semua</option>';
    priceFilter.innerHTML = '<option value="">Semua Harga</option>';

    // Populate Locations
    locations.forEach(location => {
        const option = document.createElement('option');
        option.value = location;
        option.textContent = location;
        locationFilter.appendChild(option);
    });

    // Populate Bedrooms
    bedrooms.forEach(num => {
        const option = document.createElement('option');
        option.value = num;
        option.textContent = `${num} Kamar`;
        bedroomsFilter.appendChild(option);
    });

    // Populate Bathrooms
    bathrooms.forEach(num => {
        const option = document.createElement('option');
        option.value = num;
        option.textContent = `${num} Kamar Mandi`;
        bathroomsFilter.appendChild(option);
    });

    // Populate Price Ranges (pre-defined)
    const priceRanges = [
        { label: '< 500 Juta', min: 0, max: 499999999 },
        { label: '500 Juta - 1 M', min: 500000000, max: 1000000000 },
        { label: '1 M - 2 M', min: 1000000001, max: 2000000000 },
        { label: '> 2 M', min: 2000000001, max: Infinity },
    ];

    priceRanges.forEach(range => {
        const option = document.createElement('option');
        option.value = `${range.min}-${range.max}`;
        option.textContent = range.label;
        priceFilter.appendChild(option);
    });
    
    console.log('✅ Filters populated successfully');
}

function filterProperties() {
    const location = document.getElementById('filter-location').value;
    const priceRange = document.getElementById('filter-price').value.split('-');
    const minPrice = priceRange[0] ? Number(priceRange[0]) : null;
    const maxPrice = priceRange[1] ? Number(priceRange[1]) : null;
    const bedrooms = document.getElementById('filter-bedrooms').value;
    const bathrooms = document.getElementById('filter-bathrooms').value;

    const config = window.APP_CONFIG;
    const filteredProperties = allProperties.filter(property => {
        const p = property.fields;
        const price = p[config.COLUMNS.PRICE];
        
        const locationMatch = !location || p[config.COLUMNS.LOCATION] === location;
        const priceMatch = !minPrice || (price >= minPrice && price <= maxPrice);
        const bedroomsMatch = !bedrooms || p[config.COLUMNS.BEDROOMS] == bedrooms;
        const bathroomsMatch = !bathrooms || p[config.COLUMNS.BATHROOMS] == bathrooms;
        
        return locationMatch && priceMatch && bedroomsMatch && bathroomsMatch;
    });

    renderProperties(filteredProperties, true);
}

// --- End of Filter Logic ---

// Enhanced Telegram integration with multiple fallback methods
async function sendToTelegram(message) {
    const config = window.APP_CONFIG;
    if (!config || !config.TELEGRAM_BOT_TOKEN || !config.TELEGRAM_CHAT_ID) {
        console.error('❌ Konfigurasi Telegram tidak lengkap:', {
            hasConfig: !!config,
            hasToken: !!(config && config.TELEGRAM_BOT_TOKEN),
            hasChatId: !!(config && config.TELEGRAM_CHAT_ID)
        });
        throw new Error('Gagal mengirim pesan: Konfigurasi tidak lengkap.');
    }
    
    // Check for placeholder values
    if (config.TELEGRAM_BOT_TOKEN.includes('PLACEHOLDER') || config.TELEGRAM_CHAT_ID.includes('PLACEHOLDER')) {
        console.error('❌ Menggunakan placeholder credentials untuk Telegram');
        throw new Error('Gagal mengirim pesan: Credentials belum dikonfigurasi.');
    }
    
    console.log('📨 Attempting to send message to Telegram...', config.TELEGRAM_CHAT_ID);
    
    // Try multiple methods in order of preference
    const methods = [
        {
            name: 'GET via Image',
            func: () => sendToTelegramViaGet(message, config.TELEGRAM_BOT_TOKEN, config.TELEGRAM_CHAT_ID)
        },
        {
            name: 'Direct POST',
            func: () => sendToTelegramDirect(message, config.TELEGRAM_BOT_TOKEN, config.TELEGRAM_CHAT_ID)
        },
        {
            name: 'CORS Proxy',
            func: () => sendToTelegramViaCORSProxy(message, config.TELEGRAM_BOT_TOKEN, config.TELEGRAM_CHAT_ID)
        }
    ];
    
    for (const method of methods) {
        try {
            console.log(`🔄 Trying method: ${method.name}`);
            const result = await method.func();
            console.log(`✅ Success with method: ${method.name}`);
            return result;
        } catch (error) {
            console.warn(`❌ Method ${method.name} failed:`, error.message);
            continue;
        }
    }
    
    // All methods failed, throw an informative error
    console.error('⚠️ All Telegram methods failed.');
    throw new Error('Gagal mengirim pesan: Semua metode pengiriman tidak berhasil. Mohon periksa konfigurasi dan koneksi Anda, atau coba lagi nanti.');
}

// Direct method (original implementation with enhanced error handling)
async function sendToTelegramDirect(message, botToken, chatId) {
    const url = `https://api.telegram.org/bot${botToken}/sendMessage`;
    const payload = new URLSearchParams({
        chat_id: chatId,
        text: message,
        parse_mode: 'HTML'
    });

    try {
        await fetch(url, {
            method: 'POST',
            mode: 'no-cors', // <— bypass CORS pre-flight restrictions
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: payload.toString()
        });
        return { success: true, method: 'Direct POST (no-cors)' };
    } catch (error) {
        throw new Error(error.message || 'Direct POST (no-cors) failed');
    }
}

// GET method using Image tag (works around some CORS issues)
async function sendToTelegramViaGet(message, botToken, chatId) {
    const encodedMessage = encodeURIComponent(message);
    const url = `https://api.telegram.org/bot${botToken}/sendMessage?chat_id=${chatId}&text=${encodedMessage}&parse_mode=HTML`;

    try {
        await fetch(url, { method: 'GET', mode: 'no-cors', cache: 'no-store' });
        return { success: true, method: 'GET (no-cors fetch)' };
    } catch (error) {
        throw new Error('GET (no-cors fetch) failed');
    }
}

// CORS Proxy method
async function sendToTelegramViaCORSProxy(message, botToken, chatId) {
    const corsProxies = [
        'https://api.allorigins.win/raw?url=',
        'https://corsproxy.io/?',
        'https://thingproxy.freeboard.io/fetch/' // Alternative proxy
    ];
    
    const url = `https://api.telegram.org/bot${botToken}/sendMessage`;
    const payload = {
        chat_id: chatId,
        text: message,
        parse_mode: 'HTML'
    };
    
    for (const proxy of corsProxies) {
        try {
            const proxyUrl = proxy + encodeURIComponent(url);
            const response = await fetch(proxyUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            
            const result = await response.json();
            if (result.ok) {
                return { success: true, method: `CORS Proxy (${proxy})`, result };
            }
        } catch (error) {
            console.warn(`CORS proxy ${proxy} failed:`, error.message);
            continue;
        }
    }
    
    throw new Error('All CORS proxy attempts failed');
}

// Enhanced email fallback with better formatting
function sendViaEmailFallback(message, recipientEmail = 'info@murakabiproperty.co.id') {
    const subject = encodeURIComponent('Pesan dari Website Murakabi Property');
    const body = encodeURIComponent(message.replace(/<[^>]*>/g, '')); // Remove HTML tags
    const mailtoLink = `mailto:${recipientEmail}?subject=${subject}&body=${body}`;
    
    window.open(mailtoLink, '_blank');
    return { success: true, method: 'Email Fallback' };
}

// WhatsApp fallback solution
function sendViaWhatsAppFallback(message, phoneNumber = '6281152219988') {
    // Clean HTML tags and format for WhatsApp
    const whatsappMessage = message
        .replace(/<b>/g, '*').replace(/<\/b>/g, '*')
        .replace(/<i>/g, '_').replace(/<\/i>/g, '_')
        .replace(/<[^>]*>/g, '') // Remove remaining HTML tags
        .replace(/&lt;/g, '<').replace(/&gt;/g, '>'); // Decode HTML entities
    
    const encodedMessage = encodeURIComponent(whatsappMessage);
    const whatsappLink = `https://wa.me/${phoneNumber}?text=${encodedMessage}`;
    
    window.open(whatsappLink, '_blank');
    return { success: true, method: 'WhatsApp Fallback' };
}

// Show fallback options to user
function showFallbackOptions(message) {
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
        background: rgba(0,0,0,0.8); z-index: 10000; display: flex; 
        align-items: center; justify-content: center;
    `;
    
    modal.innerHTML = `
        <div style="background: white; padding: 30px; border-radius: 10px; max-width: 500px; text-align: center;">
            <h3 style="color: #333; margin-bottom: 20px;">Pesan Tidak Dapat Dikirim Otomatis</h3>
            <p style="color: #666; margin-bottom: 30px;">Pilih cara alternatif untuk mengirim pesan Anda:</p>
            
            <div style="margin-bottom: 20px;">
                <button onclick="sendViaWhatsAppFallback('${message.replace(/'/g, "\\'")}'); this.closest('div').remove();" 
                        style="background: #25D366; color: white; padding: 15px 25px; border: none; border-radius: 5px; margin: 10px; cursor: pointer; font-size: 16px;">
                    📱 Kirim via WhatsApp
                </button>
            </div>
            
            <div style="margin-bottom: 20px;">
                <button onclick="sendViaEmailFallback('${message.replace(/'/g, "\\'")}'); this.closest('div').remove();" 
                        style="background: #007bff; color: white; padding: 15px 25px; border: none; border-radius: 5px; margin: 10px; cursor: pointer; font-size: 16px;">
                    📧 Kirim via Email
                </button>
            </div>
            
            <div>
                <button onclick="this.closest('div').remove();" 
                        style="background: #6c757d; color: white; padding: 12px 20px; border: none; border-radius: 5px; cursor: pointer;">
                    Batal
                </button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
}

// Utility to hide the property modal
function hideBuyModal() {
    const modalOverlay = document.getElementById("property-modal-overlay");
    if (modalOverlay) {
        modalOverlay.classList.remove("active");
        document.body.style.overflow = "auto";
    }
}

document.addEventListener('DOMContentLoaded', async function() {
    console.log('🚀 DOM Content Loaded');
    
    // Wait a bit for all scripts to load
    await new Promise(resolve => setTimeout(resolve, 100));
    
    console.log('🔧 Checking APP_CONFIG:', window.APP_CONFIG);
    
    // Check if APP_CONFIG is available
    if (!window.APP_CONFIG) {
        console.error('❌ APP_CONFIG not found! Waiting a bit more...');
        await new Promise(resolve => setTimeout(resolve, 500));
        if (!window.APP_CONFIG) {
            console.error('❌ APP_CONFIG still not found after waiting');
            return;
        }
    }
    
    // UI Setup from original script.js
    const navToggle = document.querySelector(".nav-toggle");
    const navMenu = document.querySelector(".nav-menu");
    if(navToggle) {
      navToggle.addEventListener("click", () => {
        navMenu.classList.toggle("active");
        const bars = navToggle.querySelectorAll(".bar");
        bars.forEach((bar, index) => {
          if (navMenu.classList.contains("active")) {
            if (index === 0) bar.style.transform = "rotate(45deg) translate(5px, 5px)";
            if (index === 1) bar.style.opacity = "0";
            if (index === 2) bar.style.transform = "rotate(-45deg) translate(7px, -6px)";
          } else {
            bar.style.transform = "none";
            bar.style.opacity = "1";
          }
        });
      });
    }
    document.querySelectorAll(".nav-link").forEach((link) => {
      link.addEventListener("click", () => {
        if(navMenu.classList.contains("active")){
            navMenu.classList.remove("active");
            const bars = navToggle.querySelectorAll(".bar");
            bars.forEach((bar) => {
                bar.style.transform = "none";
                bar.style.opacity = "1";
            });
        }
      });
    });
    window.addEventListener("scroll", () => {
      const navbar = document.querySelector(".navbar");
      if (window.scrollY > 100) navbar.classList.add("scrolled");
      else navbar.classList.remove("scrolled");
    });
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
      anchor.addEventListener("click", function (e) {
        const href = this.getAttribute("href");
        if (!href || href === '#' || !href.startsWith('#')) return; // ignore empty hash links
        e.preventDefault();
        const target = document.querySelector(href);
        if(target){
            const offsetTop = target.offsetTop - 80;
            window.scrollTo({ top: offsetTop, behavior: "smooth" });
        }
      });
    });

    // Load properties from Airtable
    console.log('📡 Starting to fetch properties from Airtable...');
    
    // First, test if filter elements are accessible
    testPopulateFilters();
    
    showLoadingState();
    try {
        // Try to get properties from Airtable, fallback to demo data if needed
        let properties;
        if (typeof getProperties === 'function') {
            properties = await getProperties();
        } else {
            properties = await fetchPropertiesFromAirtable();
        }
        
        console.log('✅ Properties fetched successfully:', properties.length, 'items');
        allProperties = properties; // Store globally
        renderProperties(allProperties, true);
        
        // Wait a bit more before populating filters
        await new Promise(resolve => setTimeout(resolve, 200));
        populateFilters(allProperties); // Populate filters with data
    } catch (error) {
        console.error('❌ Error memuat properti:', error);
        // Try fallback data as last resort
        if (window.FALLBACK_PROPERTIES) {
            console.warn('🎭 Using fallback data due to error');
            allProperties = window.FALLBACK_PROPERTIES;
            renderProperties(allProperties, true);
            populateFilters(allProperties);
        } else {
            const propertiesContainer = document.querySelector('.properties-grid');
            if (propertiesContainer) {
                propertiesContainer.innerHTML = `<div class="col-span-full text-center py-12"><p class="text-red-500">Gagal memuat properti.</p></div>`;
            }
        }
    }

    // Filter form submission
    const searchForm = document.getElementById('property-search-form');
    if (searchForm) {
        console.log('✅ Filter form found, adding event listener');
        searchForm.addEventListener('submit', (e) => {
            e.preventDefault();
            console.log('🔍 Filter form submitted');
            filterProperties();
        });
    } else {
        console.error('❌ Filter form not found');
    }

    // Modal close handlers
    const modalOverlay = document.getElementById("property-modal-overlay");
    const closeButton = document.getElementById("modal-close");
    if (modalOverlay) {
        modalOverlay.addEventListener("click", (e) => {
            if (e.target === modalOverlay) hideBuyModal();
        });
    }
    if (closeButton) {
        closeButton.addEventListener("click", hideBuyModal);
    }

    // Modal form submission
    const modalForm = document.getElementById("property-interest-form");
    if (modalForm) {
        modalForm.addEventListener("submit", async function (e) {
            e.preventDefault();
            const propertyName = document.getElementById("modal-property-title").textContent;
            const name = document.getElementById("modal-name").value;
            const phone = document.getElementById("modal-phone").value;
            
            const message = `🏠 Permintaan Pembelian Properti Baru\n\nProperti: ${propertyName}\nNama Pembeli: ${name}\nNomor Telepon: ${phone}`;
            
            const submitButton = modalForm.querySelector('button[type="submit"]');
            submitButton.textContent = 'Mengirim...';
            submitButton.disabled = true;

            try {
                await sendToTelegram(message);
                alert('Terima kasih! Tim kami akan segera menghubungi Anda.');
                this.reset();
                hideBuyModal();
            } catch (error) {
                console.error("Error sending interest form:", error);
                
                // Show enhanced fallback options
                const shouldShowFallback = confirm(
                    'Pesan tidak dapat dikirim secara otomatis. Apakah Anda ingin menggunakan cara alternatif (WhatsApp/Email)?'
                );
                
                if (shouldShowFallback) {
                    showFallbackOptions(message);
                } else {
                    alert('Permintaan gagal dikirim. Silakan coba lagi nanti atau hubungi kami langsung di 08115221998.');
                }
            } finally {
                submitButton.textContent = 'Saya Tertarik';
                submitButton.disabled = false;
            }
        });
    }

    // Contact form submission
    const contactForm = document.querySelector(".contact-form");
    if (contactForm) {
        contactForm.addEventListener("submit", async function (e) {
            e.preventDefault();
            const name = contactForm.querySelector('input[name="name"]').value;
            const email = contactForm.querySelector('input[name="email"]').value;
            const messageText = contactForm.querySelector('textarea[name="message"]').value;
            
            const message = `📧 Pesan Kontak Baru dari Website\n\nNama: ${name}\nEmail: ${email}\nPesan:\n${messageText}`;
            
            const submitButton = contactForm.querySelector('button[type="submit"]');
            const originalText = submitButton.innerHTML;
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Mengirim...';
            submitButton.disabled = true;

            try {
                await sendToTelegram(message);
                alert('Terima kasih! Pesan Anda telah terkirim. Tim kami akan segera menghubungi Anda.');
                this.reset();
            } catch (error) {
                console.error("Error sending contact form:", error);
                
                // Show enhanced fallback options
                const shouldShowFallback = confirm(
                    'Pesan tidak dapat dikirim secara otomatis. Apakah Anda ingin menggunakan cara alternatif (WhatsApp/Email)?'
                );
                
                if (shouldShowFallback) {
                    showFallbackOptions(message);
                } else {
                    alert('Pesan gagal dikirim. Silakan coba lagi nanti atau hubungi kami langsung di 08115221998.');
                }
            } finally {
                submitButton.innerHTML = originalText;
                submitButton.disabled = false;
            }
        });
    }


});
// --- End of Logic Integration --- 
// --- End of Logic from old main.js --- 