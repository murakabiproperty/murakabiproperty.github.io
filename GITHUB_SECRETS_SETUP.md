# 🔐 GitHub Secrets Setup Guide - Murakabi Property

## 📋 **QUICK SETUP**

### **Step 1: Buka GitHub Secrets**
1. Pergi ke repository Anda di GitHub
2. Klik **Settings** tab
3. Klik **Secrets and variables** > **Actions**
4. Klik **New repository secret**

### **Step 2: Copy Environment Variables**

Buka file `ENVIRONMENT_VARIABLES.txt` dan copy-paste variables berikut:

#### **✅ REQUIRED (Wajib):**

| Secret Name | Secret Value |
|-------------|--------------|
| `AIRTABLE_API_KEY` | `pat0cJUQcyOFxDllX.c2421f2ebdfeba1fdf48d662fa60ef05652a4b2deb095f5c5781362aa795c958` |
| `AIRTABLE_BASE_ID` | `appx1T49Qqh0g3AcF` |
| `TELEGRAM_BOT_TOKEN` | `7633063242:AAHKGy4bb84_nS47v3bN0OQzzT_o0dqCmNo` |
| `TELEGRAM_CHAT_ID` | `2142354455` |

#### **⚠️ OPTIONAL (Bisa ditambahkan nanti):**

| Secret Name | Secret Value |
|-------------|--------------|
| `EMAILJS_SERVICE_ID` | `your_emailjs_service_id` |
| `EMAILJS_TEMPLATE_ID` | `your_emailjs_template_id` |
| `EMAILJS_PUBLIC_KEY` | `your_emailjs_public_key` |
| `GOOGLE_MAPS_API_KEY` | `(kosong untuk sekarang)` |

### **Step 3: Test Deployment**

Setelah setup secrets:
```bash
git add .
git commit -m "Setup GitHub Secrets"
git push origin main
```

GitHub Actions akan otomatis:
- ✅ Build website dengan credentials dari secrets
- ✅ Deploy ke GitHub Pages
- ✅ Website tersedia di: `https://yourusername.github.io/repository-name`

## 🎯 **PRIORITY SETUP**

**Untuk website berfungsi minimal, setup 4 secrets ini dulu:**
1. `AIRTABLE_API_KEY`
2. `AIRTABLE_BASE_ID`  
3. `TELEGRAM_BOT_TOKEN`
4. `TELEGRAM_CHAT_ID`

**EmailJS dan Google Maps bisa ditambahkan nanti.**

## 🔍 **TROUBLESHOOTING**

### **Jika GitHub Actions gagal:**
1. Check **Actions** tab di GitHub repository
2. Klik workflow yang gagal untuk lihat error
3. Pastikan semua required secrets sudah diset
4. Pastikan nilai secrets tidak ada spasi atau karakter extra

### **Jika website tidak load data:**
1. Buka browser developer tools (F12)
2. Check console untuk error messages
3. Pastikan Airtable API key masih valid
4. Test Airtable connection di browser

## 📞 **SUPPORT**

Jika ada masalah:
1. Check `SECURITY_GUIDE.md` untuk troubleshooting
2. Check `GITHUB_PAGES_GUIDE.md` untuk deployment options
3. Check `EMERGENCY_SECURITY.md` jika ada security issues 