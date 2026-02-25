# 🚗 BMW Copart Finder - GitHub Edition

**Python yükləməyə ehtiyac yoxdur!** GitHub-da avtomatik işləyir.

## 🎯 Bu nə edir?

Hər gün avtomatik olaraq:
- Copart-da BMW 530i, 540i, M550i maşınlarını axtarır
- Sizin kriteriyalarınıza görə filtrlə
- Nəticələri email göndərir (və ya Telegram)
- JSON faylda save edir

## 🚀 Necə quraşdırım? (5 dəqiqə)

### Addım 1: GitHub hesabı yarat
1. https://github.com -a daxil ol
2. "Sign Up" bas
3. Email təsdiq et

### Addım 2: Bu repository-ni fork et
1. Bu səhifənin yuxarı sağ küncündə **"Fork"** düyməsinə bas
2. "Create fork" bas
3. İndi öz hesabınızda olacaq!

### Addım 3: Kriteriyaları dəyiş (İstəyə görə)
1. Öz repository-nizdə `copart_real_finder.py` faylını aç
2. ✏️ (edit) ikonuna bas
3. Bu bölməni tap və dəyişdir:

```python
self.criteria = {
    'models': ['530i', '540i', 'M550i'],  # Buradan dəyişdir
    'year_min': 2020,                      # Minimum il
    'year_max': 2023,                      # Maximum il
    'max_mileage': 100000,                 # Maksimum kilometr
}
```

4. **"Commit changes"** bas

### Addım 4: GitHub Actions-ı aktivləşdir
1. Repository-də **"Actions"** tabına get
2. Yaşıl düyməyə bas: **"I understand my workflows, go ahead and enable them"**

### Addım 5: İlk dəfə manual işə sal
1. Sol tərəfdə **"BMW Copart Finder"** workflow-nu seç
2. **"Run workflow"** → **"Run workflow"** bas
3. 5-10 dəqiqə gözlə

## 📊 Nəticələri necə görüm?

### Variant 1: GitHub-da bax
1. **"Actions"** tabına get
2. Ən son workflow-u aç
3. Aşağı scroll et, **"Artifacts"** bölməsində **"copart-results"** yüklə
4. ZIP-i aç, `copart_results.json` faylı orda

### Variant 2: Repository-də bax
1. Ana səhifəyə get
2. `copart_results.json` faylını aç
3. Bütün tapılan maşınlar orada

## 📧 Email bildiriş (Optional)

Yeni maşın tapıldıqda email alsınmı?

### Addım 1: Email notification scriptini əlavə et

`notify_email.py` faylını yarat:

```python
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email(results):
    sender = os.environ['EMAIL_SENDER']
    receiver = os.environ['EMAIL_RECEIVER']
    password = os.environ['EMAIL_PASSWORD']
    
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = f'🚗 Copart Alert: {len(results)} BMW tapıldı!'
    
    body = "Yeni maşınlar:\n\n"
    for i, car in enumerate(results, 1):
        body += f"{i}. {car['year']} BMW {car['model']}\n"
        body += f"   Lot: {car['lot_number']}\n"
        body += f"   VIN: {car['vin']}\n"
        body += f"   Bid: ${car['current_bid']:,}\n"
        body += f"   Link: {car['link']}\n\n"
    
    message.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(message)
    
    print("✅ Email göndərildi!")

if __name__ == "__main__":
    with open('copart_results.json', 'r') as f:
        results = json.load(f)
    
    if results:
        send_email(results)
```

### Addım 2: GitHub Secrets əlavə et

1. Repository → **"Settings"**
2. **"Secrets and variables"** → **"Actions"**
3. **"New repository secret"** bas
4. 3 secret əlavə et:
   - `EMAIL_SENDER` - sizin gmail
   - `EMAIL_RECEIVER` - göndəriləcək email
   - `EMAIL_PASSWORD` - Gmail App Password (https://myaccount.google.com/apppasswords)

### Addım 3: Workflow-u yenilə

`.github/workflows/copart-finder.yml` faylında bu sətri əlavə et:

```yaml
    - name: Send email notification
      env:
        EMAIL_SENDER: ${{ secrets.EMAIL_SENDER }}
        EMAIL_RECEIVER: ${{ secrets.EMAIL_RECEIVER }}
        EMAIL_PASSWORD: ${{ secrets.EMAIL_PASSWORD }}
      run: |
        python notify_email.py
```

## 📱 Telegram Notification (Daha asan!)

### Addım 1: Telegram bot yarat

1. Telegram-da @BotFather-ə yaz
2. `/newbot` göndər
3. Bot adını ver
4. Bot TOKEN-i save et

### Addım 2: Chat ID tap

1. Bot-a mesaj göndər
2. Bu linkə daxil ol: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
3. `chat.id` nömrəsini tap

### Addım 3: Telegram script yarat

`notify_telegram.py`:

```python
import requests
import json
import os

def send_telegram(results):
    bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    chat_id = os.environ['TELEGRAM_CHAT_ID']
    
    message = f"🚗 <b>Copart Alert: {len(results)} BMW tapıldı!</b>\n\n"
    
    for i, car in enumerate(results[:5], 1):  # İlk 5-ni göstər
        message += f"{i}. <b>{car['year']} BMW {car['model']}</b>\n"
        message += f"   💰 Bid: ${car['current_bid']:,}\n"
        message += f"   📍 {car['location']}\n"
        message += f"   🔗 <a href='{car['link']}'>Link</a>\n\n"
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    response = requests.post(url, data=data)
    print("✅ Telegram bildirişi göndərildi!")

if __name__ == "__main__":
    with open('copart_results.json', 'r') as f:
        results = json.load(f)
    
    if results:
        send_telegram(results)
```

### Addım 4: Secrets əlavə et

Repository Settings → Secrets:
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

## ⏰ Nə vaxt işləyir?

Default olaraq **hər gün səhər 09:00 UTC** (Azərbaycan vaxtı 13:00).

Dəyişmək üçün `.github/workflows/copart-finder.yml` faylında:

```yaml
schedule:
  - cron: '0 9 * * *'  # '0 21 * * *' - gecə 01:00 Azərbaycan vaxtı
```

Cron formatı:
- `0 9 * * *` - hər gün 09:00 UTC
- `0 */6 * * *` - hər 6 saatda bir
- `0 0 * * 1` - hər həftə Bazar ertəsi

## 📊 Nəticə Nümunəsi

`copart_results.json` bu şəkildə olacaq:

```json
[
  {
    "vin": "WBA53BH07PCM47363",
    "year": 2023,
    "make": "BMW",
    "model": "530i",
    "lot_number": "12345678",
    "damage": "REAR END",
    "odometer": 25000,
    "current_bid": 18500,
    "location": "HOUSTON (TX)",
    "link": "https://www.copart.com/lot/12345678",
    "airbag": "NOT DEPLOYED",
    "sale_date": "2024-03-15",
    "found_at": "2024-03-01 13:00:00"
  }
]
```

## 🔧 Troubleshooting

### Problem: Workflow işləmir

**Həll:**
1. Actions tab → en son workflow-u aç
2. Qırmızı X varsa, log-lara bax
3. Error mesajını oxu

### Problem: Results boşdur

**Səbəb:** Kriteriyaya uyğun maşın yoxdur

**Həll:**
1. Kriteriyaları genişləndir (mileage artır, il aralığını böyüt)
2. Model filterlərini azalt

### Problem: Email gəlmir

**Həll:**
1. Gmail App Password-u düzgün yaratdınızmı?
2. Secrets düzgün əlavə olunubmu?
3. Workflow log-larda email error varmı?

## 💡 Əlavə Fikirlər

### 1. Discord Notification
```python
import requests
webhook_url = "DISCORD_WEBHOOK_URL"
data = {"content": "Yeni BMW tapıldı!"}
requests.post(webhook_url, json=data)
```

### 2. Google Sheets-ə save et
```python
import gspread
# Google Sheets API istifadə et
```

### 3. WhatsApp bildirişi
Twilio API istifadə edə bilərsiniz

## 📝 Xülasə

✅ GitHub-da tam avtomatik  
✅ Python yükləməyə ehtiyac yox  
✅ Pulsuz (GitHub Actions pulsuz tier 2000 dəqiqə/ay verir)  
✅ Email/Telegram bildirişləri  
✅ Hər gün avtomatik yeniləmə  

---

**Suallarınız varmı? Issue açın və ya pull request göndərin!**

🚗 **Uğurlar!** 💨
