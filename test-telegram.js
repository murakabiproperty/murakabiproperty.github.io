// Test script for Telegram integration
// This will test if the bot token and chat ID are working

const CONFIG = {
    TELEGRAM: {
        BOT_TOKEN: '7554674052:AAEpEAx-sChhjwiLVIUlmqhbUlT46beyhew',
        CHAT_ID: '908233061'
    }
};

async function testTelegramConnection() {
    const botToken = CONFIG.TELEGRAM.BOT_TOKEN;
    const chatId = CONFIG.TELEGRAM.CHAT_ID;
    
    console.log('🔍 Testing Telegram connection...');
    console.log(`Bot Token: ${botToken.substring(0, 10)}...`);
    console.log(`Chat ID: ${chatId}`);
    
    const testMessage = `🧪 <b>TEST PESAN - MURAKABI PROPERTY</b>

✅ <b>Status:</b> Telegram integration berhasil!
🤖 <b>Bot Token:</b> Terverifikasi
📱 <b>Chat ID:</b> ${chatId}
⏰ <b>Waktu:</b> ${new Date().toLocaleString('id-ID', { timeZone: 'Asia/Jakarta' })}

---
<i>Pesan test ini dikirim untuk memverifikasi konfigurasi Telegram.</i>`;

    try {
        // Method 1: Direct POST
        console.log('📤 Trying direct POST method...');
        const url = `https://api.telegram.org/bot${botToken}/sendMessage`;
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                chat_id: chatId,
                text: testMessage,
                parse_mode: 'HTML'
            })
        });
        
        const result = await response.json();
        
        if (result.ok) {
            console.log('✅ SUCCESS: Pesan berhasil dikirim ke Telegram!');
            console.log('📋 Response:', result);
            return true;
        } else {
            console.error('❌ FAILED: Telegram API error:', result);
            return false;
        }
        
    } catch (error) {
        console.error('💥 ERROR: Network error atau masalah koneksi:', error);
        return false;
    }
}

// Run test if this is executed directly in Node.js
if (typeof window === 'undefined') {
    // Running in Node.js
    const fetch = require('node-fetch');
    testTelegramConnection();
} else {
    // Running in browser
    window.testTelegramConnection = testTelegramConnection;
} 