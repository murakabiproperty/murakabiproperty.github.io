// Konfigurasi Bot Telegram
const TELEGRAM_BOT_TOKEN = '7633063242:AAHKGy4bb84_nS47v3bN0OQzzT_o0dqCmNo';
const TELEGRAM_CHAT_ID = '2142354455';

// Konfigurasi Airtable (dimuat dari airtable-config.js)
// Pastikan untuk menyertakan airtable-config.js sebelum file ini di HTML Anda

// Fungsi API Airtable
async function fetchPropertiesFromAirtable() {
    const config = window.AIRTABLE_CONFIG;
    if (!config || !config.API_KEY || !config.BASE_ID) {
        throw new Error('Konfigurasi Airtable tidak ditemukan atau tidak lengkap');
    }
    
    const url = `https://api.airtable.com/v0/${config.BASE_ID}/${config.TABLE_NAME}`;
    console.log('🔍 Mencoba mengakses Airtable:', url);
    console.log('🔑 API Key (sebagian):', config.API_KEY.substring(0, 20) + '...');
    
    try {
        const response = await fetch(url, {
            headers: {
                'Authorization': `Bearer ${config.API_KEY}`,
                'Content-Type': 'application/json'
            }
        });

        console.log('📡 Response status:', response.status);
        console.log('📡 Response ok:', response.ok);

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
    const propertiesContainer = document.querySelector('#properties .grid');
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

function renderProperties(properties) {
    const propertiesContainer = document.querySelector('#properties .grid');
    if (!propertiesContainer) return;

    // Hapus properti yang ada
    propertiesContainer.innerHTML = '';

    if (properties.length === 0) {
        propertiesContainer.innerHTML = `
            <div class="col-span-full text-center py-12">
                <p class="text-gray-600">Tidak ada properti yang tersedia saat ini.</p>
            </div>
        `;
        return;
    }

    properties.forEach(property => {
        const fields = property.fields;
        const propertyCard = createPropertyCard(fields);
        propertiesContainer.appendChild(propertyCard);
    });
}

function createPropertyCard(fields) {
    const config = window.AIRTABLE_CONFIG;
    const cols = config ? config.COLUMNS : {};
    
    // Dapatkan nilai field menggunakan konfigurasi kolom
    const name = fields[cols.NAME] || fields.Name || 'Properti Tanpa Nama';
    const location = fields[cols.LOCATION] || fields.Location || 'Tidak ditentukan';
    const area = fields[cols.AREA] || fields.Area || 'Tidak ditentukan';
    const bedrooms = fields[cols.BEDROOMS] || fields.Bedrooms || 'Tidak ditentukan';
    const bathrooms = fields[cols.BATHROOMS] || fields.Bathrooms || 'Tidak ditentukan';
    const price = fields[cols.PRICE] || fields.Price;
    const imageField = fields[cols.IMAGE] || fields.Image;
    const mapLink = fields[cols.MAP_LINK] || fields.MapLink;
    const isSold = fields[cols.SOLD] || fields.Sold || false;
    
    const card = document.createElement('div');
    card.className = `bg-white rounded-lg shadow-lg overflow-hidden card-hover ${isSold ? 'sold-card' : ''}`;
    
    // Dapatkan URL gambar (asumsi gambar disimpan sebagai lampiran di Airtable)
    const imageUrl = imageField && imageField.length > 0 
        ? imageField[0].url 
        : 'https://via.placeholder.com/400x300';
    
    // Format harga
    const formattedPrice = formatPrice(price);
    
    card.innerHTML = `
        <div class="img-container relative">
            <img src="${imageUrl}" alt="${name}" class="w-full h-48 object-cover ${isSold ? 'sold-image' : ''}">
            ${isSold ? `
                <div class="absolute inset-0 bg-black bg-opacity-40"></div>
                <div class="absolute inset-0 flex items-center justify-center">
                    <div class="sold-badge">
                        <span class="sold-text">TERJUAL</span>
                    </div>
                </div>
            ` : ''}
        </div>
        <div class="p-6 ${isSold ? 'sold-content' : ''}">
            <h3 class="text-xl font-semibold mb-2 ${isSold ? 'text-gray-500' : ''}">${name}</h3>
            <div class="space-y-2 mb-4">
                <p class="text-gray-600"><span class="font-semibold">Lokasi:</span> ${location}</p>
                <p class="text-gray-600"><span class="font-semibold">Luas:</span> ${area} m²</p>
                <p class="text-gray-600"><span class="font-semibold">Kamar Tidur:</span> ${bedrooms}</p>
                <p class="text-gray-600"><span class="font-semibold">Kamar Mandi:</span> ${bathrooms}</p>
            </div>
            <p class="text-2xl font-bold ${isSold ? 'text-gray-400' : 'text-orange-500'} mb-4">${formattedPrice}</p>
            ${isSold ? `
                <button class="w-full bg-gray-400 text-white py-4 rounded-lg font-semibold cursor-not-allowed" disabled>
                    Sudah Terjual
                </button>
            ` : `
                <button class="buy-btn w-full bg-orange-500 text-white py-4 rounded-lg font-semibold hover:bg-orange-600 transition duration-300" 
                        data-name="${name}" data-price="${formattedPrice}" data-location="${location}" data-maplink="${mapLink || ''}">
                    Beli Sekarang
                </button>
            `}
        </div>
    `;
    
    // Add event listener for buy button
    const buyBtn = card.querySelector('.buy-btn');
    if (buyBtn) {
        buyBtn.addEventListener('click', function() {
            showBuyModal(this.dataset.name, this.dataset.price, this.dataset.location, this.dataset.maplink);
        });
    }
    
    return card;
}

function formatPrice(price) {
    if (!price) return 'Harga tidak tersedia';
    
    // Konversi harga ke format Rupiah Indonesia
    if (price >= 1000000000) {
        const billions = price / 1000000000;
        // Hanya tampilkan desimal jika ada
        return `Rp ${billions % 1 === 0 ? billions.toFixed(0) : billions.toFixed(1)} Miliar`;
    } else if (price >= 1000000) {
        const millions = price / 1000000;
        // Hanya tampilkan desimal jika ada
        return `Rp ${millions % 1 === 0 ? millions.toFixed(0) : millions.toFixed(1)} Juta`;
    } else {
        return `Rp ${price.toLocaleString('id-ID')}`;
    }
}

// Fungsi untuk membuka Google Maps dengan lokasi
function openGoogleMaps(location, propertyName) {
    if (!location || location === 'Tidak ditentukan') {
        alert('Lokasi tidak tersedia untuk properti ini.');
        return;
    }
    
    // Encode lokasi untuk URL
    const query = encodeURIComponent(`${location}, Indonesia`);
    
    // URL Google Maps
    const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${query}`;
    
    // Buka di tab baru
    window.open(mapsUrl, '_blank');
}

// Navigasi bawah mobile
document.addEventListener('DOMContentLoaded', async function() {
    // Tampilkan status loading
    showLoadingState();
    
    // Muat properti dari Airtable saat halaman dimuat
    try {
        const properties = await fetchPropertiesFromAirtable();
        renderProperties(properties);
    } catch (error) {
        console.error('Error saat memuat properti:', error);
        // Tampilkan pesan error dan fallback ke properti kosong
        const propertiesContainer = document.querySelector('#properties .grid');
        if (propertiesContainer) {
            propertiesContainer.innerHTML = `
                <div class="col-span-full text-center py-12">
                    <div class="text-red-500 mb-4">
                        <svg class="w-12 h-12 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                        </svg>
                        <h3 class="text-lg font-semibold mb-2">Gagal Memuat Properti</h3>
                        <p class="text-gray-600">Periksa koneksi Airtable Anda atau coba refresh halaman.</p>
                    </div>
                    <button onclick="window.location.reload()" class="bg-orange-500 text-white px-6 py-2 rounded-lg hover:bg-orange-600 transition-colors">
                        Coba Lagi
                    </button>
                </div>
            `;
        }
    }
    
    // Tambahkan status aktif ke navigasi bawah
    const bottomNavLinks = document.querySelectorAll('.md\\:hidden a[href^="#"]');
    
    function setActiveNavItem() {
        const currentSection = getCurrentSection();
        bottomNavLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + currentSection || 
                (currentSection === 'home' && link.getAttribute('href') === '#')) {
                link.classList.add('active');
            }
        });
    }
    
    function getCurrentSection() {
        const sections = ['properties', 'about', 'contact'];
        const scrollPos = window.scrollY + 100;
        
        if (scrollPos < 200) return 'home';
        
        for (let section of sections) {
            const element = document.getElementById(section);
            if (element) {
                const offsetTop = element.offsetTop;
                const offsetBottom = offsetTop + element.offsetHeight;
                if (scrollPos >= offsetTop && scrollPos < offsetBottom) {
                    return section;
                }
            }
        }
        return 'home';
    }
    
    // Atur status aktif awal
    setActiveNavItem();
    
    // Perbarui status aktif saat scroll
    window.addEventListener('scroll', setActiveNavItem);

    // Smooth scroll untuk tautan anchor
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                // Perbarui status aktif setelah scroll
                setTimeout(() => setActiveNavItem(), 100);
            }
        });
    });

    // Penanganan pengiriman form kontak
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const messageText = document.getElementById('message').value;

            // Format pesan untuk Telegram
            const message = `\n✉️ Pesan Baru dari Formulir Hubungi Kami Uni Property\nNama: ${name}\nEmail: ${email}\nPesan: ${messageText}`;
            try {
                await sendToTelegram(message);
                alert('Terima kasih atas pesan Anda! Tim Uni Property akan segera menghubungi Anda.');
                contactForm.reset();
            } catch (error) {
                console.error('Error saat mengirim pesan kontak:', error);
                alert('Maaf, terjadi kesalahan saat mengirim pesan Anda. Silakan coba lagi nanti.');
            }
        });
    }

    // Penanganan pengiriman form pembelian
    const buyForm = document.getElementById('buyForm');
    if (buyForm) {
        buyForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const propertyName = document.getElementById('modalPropertyName').textContent;
            const propertyPrice = document.getElementById('modalPropertyPrice').textContent;
            const buyerName = document.getElementById('buyerName').value;
            const buyerPhone = document.getElementById('buyerPhone').value;

            // Siapkan pesan untuk Telegram
            const message = `
🏠 Permintaan Pembelian Properti Baru
Properti: ${propertyName}
Harga: ${propertyPrice}
Nama Pembeli: ${buyerName}
Nomor Telepon: ${buyerPhone}
            `;

            try {
                // Kirim pesan ke Telegram
                await sendToTelegram(message);
                
                // Tampilkan pesan sukses
                alert('Terima kasih atas minat Anda! Tim kami akan segera menghubungi Anda.');
                
                // Reset form dan sembunyikan modal
                buyForm.reset();
                hideBuyModal();
            } catch (error) {
                console.error('Error saat mengirim pesan:', error);
                alert('Maaf, terjadi kesalahan saat mengirim permintaan Anda. Silakan coba lagi nanti.');
            }
        });
    }

    // Tambahkan kelas animasi ke elemen saat muncul di layar
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.animate-fade-in');
        elements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const elementBottom = element.getBoundingClientRect().bottom;
            
            if (elementTop < window.innerHeight && elementBottom > 0) {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }
        });
    };

    // Pemeriksaan awal untuk elemen yang terlihat
    animateOnScroll();

    // Periksa elemen yang terlihat saat scroll
    window.addEventListener('scroll', animateOnScroll);

    // Tambahkan efek hover ke kartu properti
    const propertyCards = document.querySelectorAll('.bg-white.rounded-lg');
    propertyCards.forEach(card => {
        card.classList.add('card-hover');
    });
});

// Fungsi modal
function showBuyModal(propertyName, propertyPrice, propertyLocation, mapLink) {
    const modal = document.getElementById('buyModal');
    document.getElementById('modalPropertyName').textContent = propertyName;
    document.getElementById('modalPropertyPrice').textContent = propertyPrice;
    document.getElementById('modalLocationText').textContent = propertyLocation || 'Lokasi tidak tersedia';
    
    // Setup map preview click handler
    const mapPreview = document.getElementById('mapPreview');
    if (mapPreview) {
        // Remove existing click handlers
        mapPreview.replaceWith(mapPreview.cloneNode(true));
        const newMapPreview = document.getElementById('mapPreview');
        
        newMapPreview.addEventListener('click', function() {
            if (mapLink && mapLink.trim() !== '') {
                // Use direct map link if available
                window.open(mapLink, '_blank');
            } else {
                // Fallback to search-based Google Maps
                openGoogleMaps(propertyLocation, propertyName);
            }
        });
    }
    
    // Add event listener to close modal when clicking on backdrop
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            hideBuyModal();
        }
    });
    
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    
    // Prevent body scroll when modal is open
    document.body.style.overflow = 'hidden';
}

function hideBuyModal() {
    const modal = document.getElementById('buyModal');
    modal.classList.add('hidden');
    modal.classList.remove('flex');
    
    // Restore body scroll when modal is closed
    document.body.style.overflow = 'auto';
}

// Integrasi Telegram
async function sendToTelegram(message) {
    const url = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`;
    
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                chat_id: TELEGRAM_CHAT_ID,
                text: message,
                parse_mode: 'HTML'
            })
        });

        if (!response.ok) {
            throw new Error('Gagal mengirim pesan ke Telegram');
        }

        return await response.json();
    } catch (error) {
        console.error('Error saat mengirim ke Telegram:', error);
        throw error;
    }
} 