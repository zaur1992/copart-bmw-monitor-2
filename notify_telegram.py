#!/usr/bin/env python3
"""
Telegram Notification for Copart Results
"""

import requests
import json
import os
import sys

def send_telegram_notification(results):
    """
    Telegram-a bildiriş göndər
    """
    
    # Environment variables-dan götür
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        print("⚠️ Telegram credentials yoxdur!")
        print("GitHub Secrets-də TELEGRAM_BOT_TOKEN və TELEGRAM_CHAT_ID əlavə edin")
        return False
    
    if not results:
        print("ℹ️ Heç bir maşın tapılmadı, bildiriş göndərilməyəcək")
        return False
    
    # Mesaj hazırla
    message = f"🚗 <b>Copart BMW Alert!</b>\n\n"
    message += f"📊 <b>{len(results)} maşın tapıldı:</b>\n\n"
    
    # İlk 5 maşını göstər (Telegram mesaj limiti 4096 simvol)
    for i, car in enumerate(results[:5], 1):
        message += f"<b>{i}. {car['year']} BMW {car['model']}</b>\n"
        message += f"   🏷 Lot: <code>{car['lot_number']}</code>\n"
        message += f"   🔢 VIN: <code>{car['vin']}</code>\n"
        message += f"   💥 Damage: {car.get('damage', 'N/A')}\n"
        message += f"   🎈 Airbag: {car.get('airbag', 'N/A')}\n"
        message += f"   📏 Odometer: {car['odometer']:,} mil\n"
        message += f"   💰 Current Bid: <b>${car['current_bid']:,}</b>\n"
        message += f"   📍 Location: {car['location']}\n"
        message += f"   🔗 <a href='{car['link']}'>Copart Link</a>\n\n"
    
    if len(results) > 5:
        message += f"<i>... və daha {len(results) - 5} maşın</i>\n\n"
    
    message += f"⏰ <i>Son yoxlanma: {results[0].get('found_at', 'N/A')}</i>"
    
    # Telegram API
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    data = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML',
        'disable_web_page_preview': False
    }
    
    try:
        response = requests.post(url, data=data, timeout=10)
        
        if response.status_code == 200:
            print("✅ Telegram bildirişi uğurla göndərildi!")
            return True
        else:
            print(f"❌ Telegram xətası: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Xəta: {e}")
        return False


def send_summary_message(total_found, filtered_count):
    """
    Xülasə mesajı göndər
    """
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        return
    
    message = "📋 <b>Copart Axtarış Xülasəsi</b>\n\n"
    message += f"🔍 Tapılan: {total_found} maşın\n"
    message += f"✅ Filtrdən keçən: {filtered_count} maşın\n"
    
    if filtered_count == 0:
        message += "\n⚠️ Kriteriyanıza uyğun maşın yoxdur"
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    requests.post(url, data=data, timeout=10)


if __name__ == "__main__":
    # JSON fayldan oxu
    try:
        with open('copart_results.json', 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        if results:
            success = send_telegram_notification(results)
            if success:
                sys.exit(0)
            else:
                sys.exit(1)
        else:
            print("ℹ️ Nəticə faylı boşdur")
            send_summary_message(0, 0)
            sys.exit(0)
            
    except FileNotFoundError:
        print("❌ copart_results.json faylı tapılmadı!")
        sys.exit(1)
    except json.JSONDecodeError:
        print("❌ JSON parse xətası!")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Xəta: {e}")
        sys.exit(1)
