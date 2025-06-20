# 🔐 Panduan Keamanan - Murakabi Property Website

## ⚠️ PENTING: Mengamankan Informasi Sensitif

Website static memiliki tantangan khusus dalam mengamankan data sensitif karena semua kode berjalan di browser client. Berikut adalah strategi untuk mengamankan API keys, tokens, dan informasi confidential lainnya.

## 🚫 **JANGAN PERNAH LAKUKAN INI**

```javascript
// ❌ JANGAN: Hardcode API keys di kode
const API_KEY = "pat_abcd1234567890"; // Ini akan terlihat semua orang!
const BOT_TOKEN = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"; // Sangat berbahaya!
```

## ✅ **STRATEGI KEAMANAN YANG DIREKOMENDASIKAN**

### 1. **Environment Variables + Build Process**

```bash
# .env file (JANGAN commit ke Git)
AIRTABLE_API_KEY=pat_your_real_api_key_here
TELEGRAM_BOT_TOKEN=your_real_bot_token_here
TELEGRAM_CHAT_ID=your_real_chat_id_here
```

```javascript
// Gunakan build tools seperti Vite, Webpack, atau Parcel
const config = {
    airtableKey: import.meta.env.VITE_AIRTABLE_API_KEY,
    telegramToken: import.meta.env.VITE_TELEGRAM_BOT_TOKEN
};
```

### 2. **Server-Side Proxy/Middleware (TERBAIK)**

Buat backend sederhana untuk handle API calls:

```javascript
// backend/server.js (Node.js/Express)
app.post('/api/contact', (req, res) => {
    // API keys disimpan di server, tidak di client
    const response = await fetch('https://api.airtable.com/v0/...', {
        headers: {
            'Authorization': `Bearer ${process.env.AIRTABLE_API_KEY}`
        }
    });
    res.json(response);
});
```

### 3. **Serverless Functions**

```javascript
// netlify/functions/contact.js
exports.handler = async (event, context) => {
    const airtableKey = process.env.AIRTABLE_API_KEY;
    // Handle API call dengan key yang aman di server
};
```

### 4. **Third-Party Services untuk Static Sites**

#### A. EmailJS (Untuk Contact Forms)
```javascript
// Public keys EmailJS aman untuk digunakan di client
emailjs.init("your_public_key"); // Public key, aman
emailjs.send("service_id", "template_id", templateParams);
```

#### B. Formspree
```html
<!-- Formspree endpoint aman untuk digunakan langsung -->
<form action="https://formspree.io/f/your_form_id" method="POST">
```

#### C. Netlify Forms
```html
<!-- Built-in Netlify forms -->
<form name="contact" method="POST" data-netlify="true">
```

## 🛡️ **IMPLEMENTASI UNTUK MURAKABI PROPERTY**

### 1. **Setup Environment Variables**

```bash
# Copy example file
cp .env.example .env

# Edit dengan nilai real Anda
nano .env
```

### 2. **Update airtable-config.js**

```javascript
// js/airtable-config.js
const AIRTABLE_CONFIG = {
    API_KEY: CONFIG.AIRTABLE.API_KEY, // Dari config.js
    BASE_ID: CONFIG.AIRTABLE.BASE_ID,
    TABLE_NAME: CONFIG.AIRTABLE.TABLE_NAME,
    // ... rest of config
};
```

### 3. **Secure Contact Form**

```javascript
// Gunakan EmailJS atau Formspree
async function submitContactForm(formData) {
    try {
        // Option 1: EmailJS
        await emailjs.send(
            CONFIG.CONTACT.EMAILJS.SERVICE_ID,
            CONFIG.CONTACT.EMAILJS.TEMPLATE_ID,
            formData,
            CONFIG.CONTACT.EMAILJS.PUBLIC_KEY
        );
        
        // Option 2: Formspree
        await fetch(CONFIG.CONTACT.FORMSPREE.ENDPOINT, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
    } catch (error) {
        console.error('Error sending form:', error);
    }
}
```

## 🚀 **DEPLOYMENT STRATEGIES**

### 1. **Netlify**
```bash
# Set environment variables di Netlify dashboard
# Site settings > Environment variables
AIRTABLE_API_KEY=your_key_here
TELEGRAM_BOT_TOKEN=your_token_here
```

### 2. **Vercel**
```bash
# Set di Vercel dashboard atau CLI
vercel env add AIRTABLE_API_KEY
```

### 3. **GitHub Pages + Actions**
```yaml
# .github/workflows/deploy.yml
env:
  AIRTABLE_API_KEY: ${{ secrets.AIRTABLE_API_KEY }}
  TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
```

## 🔍 **AUDIT KEAMANAN**

### Checklist Sebelum Deploy:
- [ ] Tidak ada hardcoded API keys di kode
- [ ] File .env tidak ter-commit ke Git
- [ ] .gitignore includes .env dan config.js
- [ ] Environment variables set di hosting platform
- [ ] API keys memiliki scope/permissions minimal
- [ ] Rate limiting enabled di API providers

### Tools untuk Scan:
```bash
# Scan for secrets in code
npm install -g truffleHog
trufflehog --regex --entropy=False .

# GitHub secret scanning (otomatis)
# GitLab secret detection (otomatis)
```

## 📞 **CONTACT FORM SECURITY**

### Recommended: EmailJS Setup
1. Daftar di [EmailJS.com](https://emailjs.com)
2. Setup email service (Gmail, Outlook, etc.)
3. Create email template
4. Get public key (aman untuk client-side)

```javascript
// Setup EmailJS
emailjs.init("your_public_key_here");

// Send email
emailjs.send("gmail", "contact_form", {
    from_name: formData.name,
    from_email: formData.email,
    message: formData.message,
    to_email: "info@murakabiproperty.co.id"
});
```

## ⚡ **QUICK START AMAN**

1. **Copy config example:**
```bash
cp js/config.example.js js/config.js
```

2. **Edit dengan nilai real Anda:**
```bash
nano js/config.js
```

3. **Pastikan .gitignore aktif:**
```bash
git status # config.js tidak boleh muncul
```

4. **Deploy dengan environment variables di hosting platform**

## 🆘 **JIKA CREDENTIALS SUDAH TERLANJUR LEAK**

1. **Immediately revoke/regenerate:**
   - Airtable: Generate new Personal Access Token
   - Telegram: Revoke bot token via @BotFather
   - Email services: Generate new API keys

2. **Remove from Git history:**
```bash
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch js/airtable-config.js' --prune-empty --tag-name-filter cat -- --all
```

3. **Force push:**
```bash
git push origin --force --all
```

## 📚 **RESOURCES**

- [OWASP API Security](https://owasp.org/www-project-api-security/)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [Netlify Environment Variables](https://docs.netlify.com/configure-builds/environment-variables/)
- [EmailJS Documentation](https://www.emailjs.com/docs/)

---

**💡 TIP:** Untuk website properti seperti Murakabi Property, gunakan kombinasi EmailJS untuk contact forms dan serverless functions untuk Airtable API calls untuk keamanan maksimal. 