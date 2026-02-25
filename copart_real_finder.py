#!/usr/bin/env python3
"""
Copart BMW G30 Real-Time Finder
REAL Copart API ilə işləyir (Selenium istifadə edir)
"""

import time
import json
from datetime import datetime
from typing import List, Dict, Optional

# Bu libraryləri install etmək lazımdır:
# pip install selenium webdriver-manager requests

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
except ImportError:
    print("⚠️ SELENIUM QURAŞDIRILMAYIB!")
    print("📦 Install etmək üçün:")
    print("   pip install selenium webdriver-manager")
    print()


class CopartRealFinder:
    """Real-time Copart scraper"""
    
    def __init__(self):
        self.base_url = "https://www.copart.com"
        
        # Chrome options
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')  # Görünməz rejim
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        # Sizin kriteriyalar
        self.criteria = {
            'make': 'BMW',
            'models': ['530i', '540i', 'M550i'],
            'year_min': 2020,
            'year_max': 2023,
            'exclude_front_damage': True,
            'airbag_not_deployed': True,
            'max_mileage': 100000,  # maksimum kilometr
            'min_year': 2020
        }
    
    def init_driver(self):
        """Chrome driver başlat"""
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=self.chrome_options)
            return driver
        except Exception as e:
            print(f"❌ Driver xətası: {e}")
            return None
    
    def search_copart(self) -> List[Dict]:
        """
        Copart-da real axtarış
        """
        driver = self.init_driver()
        if not driver:
            return []
        
        try:
            print("🔍 Copart.com-a daxil olunur...")
            
            # Copart ana səhifə
            driver.get(self.base_url)
            time.sleep(3)
            
            # Search bölməsinə get
            search_url = f"{self.base_url}/vehicleFinder/"
            driver.get(search_url)
            time.sleep(3)
            
            # Make filter (BMW)
            print("🔍 BMW-lər axtarılır...")
            make_filter = driver.find_element(By.ID, "make-filter")
            make_filter.send_keys("BMW")
            time.sleep(2)
            
            # Model filter
            for model in self.criteria['models']:
                try:
                    model_input = driver.find_element(By.ID, "model-filter")
                    model_input.send_keys(model)
                    time.sleep(1)
                except:
                    continue
            
            # Year filter
            year_from = driver.find_element(By.ID, "year-from")
            year_from.send_keys(str(self.criteria['year_min']))
            
            year_to = driver.find_element(By.ID, "year-to")
            year_to.send_keys(str(self.criteria['year_max']))
            time.sleep(1)
            
            # Search button
            search_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            search_btn.click()
            time.sleep(5)
            
            # Nəticələri götür
            vehicles = self.parse_results(driver)
            
            print(f"✅ {len(vehicles)} maşın tapıldı")
            return vehicles
            
        except Exception as e:
            print(f"❌ Xəta: {e}")
            return []
        finally:
            driver.quit()
    
    def parse_results(self, driver) -> List[Dict]:
        """
        Nəticələri parse et
        """
        vehicles = []
        
        try:
            # Wait for results
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "vehicle-card"))
            )
            
            # Bütün vehicle card-ları tap
            cards = driver.find_elements(By.CLASS_NAME, "vehicle-card")
            
            for card in cards:
                try:
                    vehicle = self.parse_vehicle_card(card)
                    if vehicle:
                        vehicles.append(vehicle)
                except Exception as e:
                    print(f"⚠️ Card parse xətası: {e}")
                    continue
            
        except Exception as e:
            print(f"❌ Results parse xətası: {e}")
        
        return vehicles
    
    def parse_vehicle_card(self, card) -> Optional[Dict]:
        """
        Bir vehicle card-ı parse et
        """
        try:
            # VIN
            vin = card.find_element(By.CLASS_NAME, "vin").text
            
            # Year, Make, Model
            title = card.find_element(By.CLASS_NAME, "vehicle-title").text
            parts = title.split()
            year = int(parts[0])
            make = parts[1]
            model = ' '.join(parts[2:])
            
            # Lot number
            lot = card.find_element(By.CLASS_NAME, "lot-number").text
            
            # Damage
            damage = card.find_element(By.CLASS_NAME, "damage-type").text
            
            # Odometer
            odometer_text = card.find_element(By.CLASS_NAME, "odometer").text
            odometer = int(''.join(filter(str.isdigit, odometer_text)))
            
            # Current bid
            try:
                bid_text = card.find_element(By.CLASS_NAME, "current-bid").text
                current_bid = int(''.join(filter(str.isdigit, bid_text)))
            except:
                current_bid = 0
            
            # Location
            location = card.find_element(By.CLASS_NAME, "location").text
            
            # Link
            link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
            
            vehicle = {
                'vin': vin,
                'year': year,
                'make': make,
                'model': model,
                'lot_number': lot,
                'damage': damage,
                'odometer': odometer,
                'current_bid': current_bid,
                'location': location,
                'link': link,
                'found_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return vehicle
            
        except Exception as e:
            print(f"⚠️ Vehicle parse xətası: {e}")
            return None
    
    def filter_vehicles(self, vehicles: List[Dict]) -> List[Dict]:
        """
        Kriteriyalara görə filtrlə
        """
        filtered = []
        
        for v in vehicles:
            # Front damage yoxla
            if self.criteria['exclude_front_damage']:
                if 'FRONT' in v['damage'].upper():
                    print(f"   ❌ {v['lot_number']} - Front damage")
                    continue
            
            # Mileage yoxla
            if v['odometer'] > self.criteria['max_mileage']:
                print(f"   ❌ {v['lot_number']} - Çox kilometr ({v['odometer']})")
                continue
            
            # Model yoxla
            model_match = False
            for model in self.criteria['models']:
                if model in v['model']:
                    model_match = True
                    break
            
            if not model_match:
                print(f"   ❌ {v['lot_number']} - Model uyğun deyil")
                continue
            
            print(f"   ✅ {v['lot_number']} - Uyğundur!")
            filtered.append(v)
        
        return filtered
    
    def get_vehicle_details(self, vehicle: Dict) -> Dict:
        """
        Maşın haqqında ətraflı məlumat (VIN link-dən)
        """
        driver = self.init_driver()
        if not driver:
            return vehicle
        
        try:
            print(f"🔍 Detallar yüklənir: {vehicle['lot_number']}")
            driver.get(vehicle['link'])
            time.sleep(3)
            
            # Airbag status
            try:
                airbag_elem = driver.find_element(By.XPATH, "//dt[text()='Airbags']/following-sibling::dd[1]")
                vehicle['airbag'] = airbag_elem.text
            except:
                vehicle['airbag'] = 'UNKNOWN'
            
            # Title
            try:
                title_elem = driver.find_element(By.XPATH, "//dt[text()='Title']/following-sibling::dd[1]")
                vehicle['title'] = title_elem.text
            except:
                vehicle['title'] = 'UNKNOWN'
            
            # Sale date
            try:
                sale_elem = driver.find_element(By.CLASS_NAME, "sale-date")
                vehicle['sale_date'] = sale_elem.text
            except:
                vehicle['sale_date'] = 'UNKNOWN'
            
            # Images count
            try:
                images = driver.find_elements(By.CLASS_NAME, "thumbnail")
                vehicle['images_count'] = len(images)
            except:
                vehicle['images_count'] = 0
            
            return vehicle
            
        except Exception as e:
            print(f"❌ Detal xətası: {e}")
            return vehicle
        finally:
            driver.quit()
    
    def save_results(self, vehicles: List[Dict], filename: str = "copart_results.json"):
        """
        Nəticələri JSON-a save et
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(vehicles, f, indent=2, ensure_ascii=False)
            print(f"💾 Nəticələr save edildi: {filename}")
        except Exception as e:
            print(f"❌ Save xətası: {e}")
    
    def run(self):
        """
        Əsas proqram
        """
        print("="*80)
        print("🚗 BMW G30 REAL-TIME COPART FINDER")
        print("="*80)
        print("\n📋 KRİTERİYALAR:")
        print(f"   Modellər: {', '.join(self.criteria['models'])}")
        print(f"   İl: {self.criteria['year_min']}-{self.criteria['year_max']}")
        print(f"   Front damage: {'Yox' if self.criteria['exclude_front_damage'] else 'Ola bilər'}")
        print(f"   Max kilometr: {self.criteria['max_mileage']:,}")
        print()
        
        # Axtarış
        vehicles = self.search_copart()
        
        if not vehicles:
            print("\n❌ Heç bir maşın tapılmadı!")
            return
        
        # Filtrlə
        print(f"\n📊 FİLTRLƏMƏ:")
        filtered = self.filter_vehicles(vehicles)
        print(f"\n✅ {len(filtered)} uyğun maşın tapıldı")
        
        if not filtered:
            print("\n❌ Kriteriyanıza uyğun maşın yoxdur!")
            return
        
        # Hər birinin detallarını götür
        print("\n📝 DETAL MƏLUMATLAR:")
        detailed = []
        for vehicle in filtered:
            detailed_vehicle = self.get_vehicle_details(vehicle)
            detailed.append(detailed_vehicle)
        
        # Save et
        self.save_results(detailed)
        
        # Nəticələri göstər
        print("\n" + "="*80)
        print("📊 TAPILAN MAŞINLAR")
        print("="*80)
        
        for i, v in enumerate(detailed, 1):
            print(f"\n{i}. {v['year']} BMW {v['model']}")
            print(f"   Lot: {v['lot_number']}")
            print(f"   VIN: {v['vin']}")
            print(f"   Damage: {v['damage']}")
            print(f"   Airbag: {v.get('airbag', 'UNKNOWN')}")
            print(f"   Kilometr: {v['odometer']:,} mil")
            print(f"   Cari bid: ${v['current_bid']:,}")
            print(f"   Yer: {v['location']}")
            print(f"   Link: {v['link']}")
        
        print("\n" + "="*80)
        print("✅ Tamamlandı!")
        print(f"📁 Nəticələr: copart_results.json")
        print("="*80)


if __name__ == "__main__":
    try:
        finder = CopartRealFinder()
        finder.run()
    except KeyboardInterrupt:
        print("\n\n⚠️ Proqram dayandırıldı!")
    except Exception as e:
        print(f"\n❌ Xəta: {e}")
