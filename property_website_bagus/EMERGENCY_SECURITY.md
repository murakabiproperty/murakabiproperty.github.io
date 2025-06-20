# 🚨 EMERGENCY SECURITY RESPONSE

## ⚠️ JIKA CREDENTIALS SUDAH TERLANJUR LEAK KE GIT

### 🔥 **TINDAKAN SEGERA (DALAM 5 MENIT)**

1. **Revoke/Regenerate SEMUA credentials:**

#### Airtable:
```bash
# 1. Login ke Airtable.com
# 2. Go to Account > Developer hub > Personal access tokens
# 3. Delete token: pat0cJUQcyOFxDllX.c2421f2ebdfeba1fdf48d662fa60ef05652a4b2deb095f5c5781362aa795c958
# 4. Generate new token dengan scope minimal
```

#### Telegram Bot:
```bash
# 1. Chat dengan @BotFather di Telegram
# 2. Send: /revoke
# 3. Select bot: @your_bot_name
# 4. Generate new token
```

### 🧹 **CLEAN UP GIT HISTORY**

```bash
# 1. Remove sensitive file from Git history
git filter-branch --force --index-filter \
'git rm --cached --ignore-unmatch js/airtable-config.js' \
--prune-empty --tag-name-filter cat -- --all

# 2. Force push to overwrite history
git push origin --force --all

# 3. Clean local repository
git for-each-ref --format='delete %(refname)' refs/original | git update-ref --stdin
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

### 🔒 **SECURE SETUP BARU**

```bash
# 1. Setup secure configuration
cp js/config.example.js js/config.js

# 2. Edit dengan credentials BARU
nano js/config.js

# 3. Verify .gitignore
git status # config.js tidak boleh muncul

# 4. Test website
# 5. Deploy dengan environment variables
```

## 📞 **CONTACT EMERGENCY**

Jika Anda membutuhkan bantuan segera:
- Email: security@murakabiproperty.co.id
- WhatsApp: +62-xxx-xxx-xxxx

## 🛡️ **PREVENTION CHECKLIST**

- [ ] .gitignore includes js/config.js
- [ ] No hardcoded credentials in any file
- [ ] Environment variables set di hosting platform
- [ ] Regular security audit
- [ ] Team training on security practices

---

**⏰ REMEMBER:** Semakin cepat Anda bertindak, semakin aman sistem Anda! 