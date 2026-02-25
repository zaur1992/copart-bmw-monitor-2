# 🚗 BMW Copart Finder - QUICK START

## ⚡ 5 Dəqiqəyə Quraşdırma (Python-suz!)

### ✅ Sizə lazım olan:
1. GitHub hesabı (pulsuz)
2. Email və ya Telegram (bildirişlər üçün)

---

## 📱 VARIANT 1: Telegram ilə (ƏN ASAN!)

### 1️⃣ GitHub-da Fork edin
1. https://github.com adresinə daxil olun (hesab yaradın)
2. Bu repository-ni tapın (və ya link göndərdim)
3. Yuxarı sağda **"Fork"** düyməsinə basın
4. **"Create fork"** basın

### 2️⃣ Telegram Bot yaradın
1. Telegram-da **@BotFather** tapın
2. `/newbot` göndərin
3. Bot adını yazın (məsələn: "MyCopartBot")
4. Username yazın (məsələn: "my_copart_bot")
5. **TOKEN-i save edin** (məsələn: `123456:ABC-DEF1234...`)

### 3️⃣ Chat ID tapın
1. Bot-a "salam" yazın
2. Bu linkə daxil olun (TOKEN-i dəyişdirin):
   ```
   https://api.telegram.org/bot123456:ABC-DEF1234.../getUpdates
   ```
3. `"chat":{"id":` hissəsində rəqəmi tapın (məsələn: `987654321`)

### 4️⃣ GitHub-da Secrets əlavə edin
1. Öz fork-unuzda **"Settings"** → **"Secrets and variables"** → **"Actions"**
2. **"New repository secret"** basın
3. İki secret əlavə edin:
   
   **Secret 1:**
   - Name: `TELEGRAM_BOT_TOKEN`
   - Value: `123456:ABC-DEF1234...` (sizin token)
   
   **Secret 2:**
   - Name: `TELEGRAM_CHAT_ID`
   - Value: `987654321` (sizin chat ID)

### 5️⃣ İşə salın!
1. **"Actions"** tabına keçin
2. Yaşıl düyməyə basın: **"I understand my workflows..."**
3. Sol tərəfdə **"BMW Copart Finder"** seçin
4. **"Run workflow"** → **"Run workflow"** basın
5. 5-10 dəqiqə gözləyin
6. Telegram-a bildiriş gələcək! 🎉

---

## 📧 VARIANT 2: Email ilə

### 1-4 addımlar eynidir (Fork, Bot, Secrets)

### 5️⃣ Gmail App Password yaradın
1. https://myaccount.google.com/apppasswords
2. "App name" yazın (məsələn: "Copart")
3. **Password-u save edin** (məsələn: `abcd efgh ijkl mnop`)

### 6️⃣ GitHub Secrets
Əlavə 3 secret:
- `EMAIL_SENDER`: sizin gmail (məsələn: `name@gmail.com`)
- `EMAIL_RECEIVER`: göndəriləcək email
- `EMAIL_PASSWORD`: app password (`abcd efgh ijkl mnop`)

### 7️⃣ Workflow faylını yenilə
`.github/workflows/copart-finder.yml` faylında bu sətri əlavə edin:
```yaml
    - name: Send email
      env:
        EMAIL_SENDER: ${{ secrets.EMAIL_SENDER }}
        EMAIL_RECEIVER: ${{ secrets.EMAIL_RECEIVER }}
        EMAIL_PASSWORD: ${{ secrets.EMAIL_PASSWORD }}
      run: python notify_email.py
```

---

## ⚙️ KRİTERİYALARI DƏYİŞMƏK

### GitHub web interface-də:
1. `copart_real_finder.py` faylını açın
2. ✏️ **Edit** ikonuna basın
3. Bu bölməni tapın və dəyişdirin:

```python
self.criteria = {
    'models': ['530i', '540i', 'M550i'],  # ← Buradan dəyişdir
    'year_min': 2020,                      # ← Minimum il
    'year_max': 2023,                      # ← Maximum il
    'max_mileage': 100000,                 # ← Max kilometr
    'exclude_front_damage': True,         # False = front damage ola bilər
    'airbag_not_deployed': True,          # False = airbag açıla bilər
}
```

4. **"Commit changes"** basın
5. Növbəti workflow avtomatik yeni kriteriya ilə işləyəcək!

---

## ⏰ NƏ VAXT İŞLƏYİR?

Default: **Hər gün səhər 09:00 UTC** (Azərbaycan 13:00)

### Dəyişmək üçün:
`.github/workflows/copart-finder.yml` faylında:

```yaml
schedule:
  - cron: '0 9 * * *'  # Bu sətri dəyişdir
```

**Cron nümunələri:**
- `0 21 * * *` → Hər gün 21:00 UTC (Azərbaycan 01:00)
- `0 */6 * * *` → Hər 6 saatda bir
- `0 9 * * 1` → Hər həftə Bazar ertəsi
- `0 9 * * 1,4` → Bazar ertəsi və Cümə axşamı

---

## 📊 NƏTİCƏLƏRİ GÖRÜNTÜLƏ

### GitHub-da:
1. **"Actions"** tab
2. Ən son workflow-u aç
3. **"Artifacts"** bölməsində **"copart-results"** ZIP yüklə

### Repository-də:
1. Ana səhifə
2. `copart_results.json` faylı
3. Maşınların JSON listi

---

## 🐛 PROBLEM OLDU?

### Workflow işləmir:
- **Actions** → ən son workflow → **logs-a bax**
- Qırmızı error mesajını oxu

### Results boşdur:
- Normal! Kriteriyanıza uyğun maşın olmaya bilər
- Kriteriyaları genişləndir (mileage artır, il aralığı böyüt)

### Telegram gəlmir:
- Bot TOKEN düzgündür?
- Chat ID düzgündür?
- Secrets düzgün əlavə olunub?
- Bot-a "salam" yazmısınız? (vacib!)

---

## 🎯 ÖZƏT

1. ✅ GitHub-da fork et
2. ✅ Telegram bot yarat
3. ✅ Secrets əlavə et
4. ✅ Workflow işə sal
5. ✅ Gözlə (5-10 dəq)
6. ✅ Telegram-a bildiriş gələcək!

**Hər gün avtomatik yoxlanacaq və sizə bildiriş göndərəcək!**

---

## 💡 ƏLAVƏ FIKIRLƏR

### Discord notification:
```python
webhook = "DISCORD_WEBHOOK_URL"
requests.post(webhook, json={"content": "BMW tapıldı!"})
```

### WhatsApp (Twilio):
```python
from twilio.rest import Client
client.messages.create(body="BMW!", from_="...", to="...")
```

### Birbaşa tender (Copart API):
```python
# DİQQƏT: Copart qaydalarına uyğun olmalı!
def place_bid(lot, amount):
    # Copart API
    pass
```

---

## 🆘 HELP

Sualınız var? 
1. README.md-yə bax (ətraflı guide)
2. GitHub Issues-də soruş
3. Pull request göndər

---

**🚗 Uğurlar! İndi hər gün avtomatik Copart axtarışınız var! 🎉**
