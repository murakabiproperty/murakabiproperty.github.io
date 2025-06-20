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
                ${area} m²
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
    const area = fields[cols.AREA] ? `${fields[cols.AREA]} m²` : "-";
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

async function sendToTelegram(message) {
    const config = window.APP_CONFIG;
    if (!config || !config.TELEGRAM_BOT_TOKEN || !config.TELEGRAM_CHAT_ID) {
        console.error('Konfigurasi Telegram tidak lengkap.');
        throw new Error('Gagal mengirim pesan: Konfigurasi tidak lengkap.');
    }
    const url = `https://api.telegram.org/bot${config.TELEGRAM_BOT_TOKEN}/sendMessage`;
    
    try {
        const payload = {
            chat_id: config.TELEGRAM_CHAT_ID,
            text: message,
            parse_mode: 'HTML'
        };
        console.log('📨 Sending Telegram payload:', payload);

        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await response.json().catch(() => null);
        console.log('🤖 Telegram response status:', response.status, result);

        if (!response.ok || (result && result.ok === false)) {
            const errMsg = result && result.description ? result.description : 'Unknown Telegram API error';
            throw new Error(`Gagal mengirim pesan ke Telegram: ${errMsg}`);
        }
        return result;
    } catch (error) {
        console.error('❌ Error saat mengirim ke Telegram:', error);
        throw error;
    }
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
        const properties = await fetchPropertiesFromAirtable();
        console.log('✅ Properties fetched successfully:', properties.length, 'items');
        allProperties = properties; // Store globally
        renderProperties(allProperties, true);
        
        // Wait a bit more before populating filters
        await new Promise(resolve => setTimeout(resolve, 200));
        populateFilters(allProperties); // Populate filters with data
    } catch (error) {
        console.error('❌ Error memuat properti:', error);
        const propertiesContainer = document.querySelector('.properties-grid');
        if (propertiesContainer) {
            propertiesContainer.innerHTML = `<div class="col-span-full text-center py-12"><p class="text-red-500">Gagal memuat properti.</p></div>`;
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
                alert('Gagal mengirim permintaan. Silakan coba lagi.');
            } finally {
                submitButton.textContent = 'Saya Tertarik';
                submitButton.disabled = false;
            }
        });
    }

    // Contact form submission
    const contactForm = document.querySelector('.contact-form');
    if(contactForm){
        contactForm.addEventListener('submit', async function(e){
            e.preventDefault();
            const name = this.querySelector('input[placeholder="Nama Anda"]').value;
            const email = this.querySelector('input[placeholder="Email Anda"]').value;
            const messageText = this.querySelector('textarea').value;
            
            const message = `✉️ Pesan Baru dari Formulir Kontak\n\nNama: ${name}\nEmail: ${email}\nPesan:\n${messageText}`;

            const submitButton = contactForm.querySelector('button[type="submit"]');
            const originalButtonHTML = submitButton.innerHTML;
            submitButton.innerHTML = 'Mengirim...';
            submitButton.disabled = true;

            try {
                await sendToTelegram(message);
                alert('Terima kasih! Pesan Anda telah terkirim.');
                this.reset();
            } catch(error) {
                alert('Gagal mengirim pesan. Silakan coba lagi.');
            } finally {
                submitButton.innerHTML = originalButtonHTML;
                submitButton.disabled = false;
            }
        });
    }
});
// --- End of Logic Integration --- 
// --- End of Logic from old main.js --- 