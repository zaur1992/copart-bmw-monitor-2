#!/usr/bin/env python3
"""
Copart BMW G30 Finder
Sizin kriteriyalarınıza görə BMW 5-Series (G30) maşınları tapır
"""

import requests
import json
from datetime import datetime
from typing import List, Dict, Optional

class CopartBMWFinder:
    """Copart-da BMW axtarışı"""
    
    def __init__(self):
        self.base_url = "https://www.copart.com"
        self.api_url = "https://www.copart.com/public/vehiclefinder/search"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
        }
        
        # SİZİN KRİTERİYALARINIZ
        self.criteria = {
            'make': 'BMW',
            'model': ['530i', '540i', 'M550i'],  # 5-Series models
            'year_min': 2020,
            'year_max': 2023,
            'series': 'G30',
            
            # Damage kriteriləri
            'exclude_front_damage': True,
            'airbag_not_deployed': True,
            
            # Wanted opsiyalar
            'wanted_options': [
                'Driving Assistant Professional',
                'Harman Kardon',
                'Bowers & Wilkins',
                'Soft Close'
            ]
        }
    
    def search_vehicles(self) -> List[Dict]:
        """
        Copart-da BMW 5-Series axtarır
        """
        
        # Axtarış parametrləri
        search_params = {
            'query': 'BMW 530i 540i M550i',
            'filter': {
                'YEAR': f'{self.criteria["year_min"]}-{self.criteria["year_max"]}',
                'MAKE': ['ABMW'],  # Copart BMW kodu
                'MISC': ['frontEnd-NotDamaged', 'airbag-NotDeployed']  # Filerlər
            },
            'size': 100,
            'sort': 'auction_date_type=asc,auction_date_utc=asc'
        }
        
        try:
            print("🔍 Copart-da axtarış aparılır...")
            
            # API request (real implementasiya üçün session və authentication lazımdır)
            # response = requests.post(self.api_url, json=search_params, headers=self.headers)
            
            # DEMO məlumat (real API üçün uncomment edin)
            vehicles = self._demo_results()
            
            print(f"✅ {len(vehicles)} maşın tapıldı")
            return vehicles
            
        except Exception as e:
            print(f"❌ Xəta: {e}")
            return []
    
    def _demo_results(self) -> List[Dict]:
        """Demo nəticələr (test üçün)"""
        return [
            {
                'lot_number': '12345678',
                'vin': 'WBA53BH07PCM47363',
                'year': 2023,
                'make': 'BMW',
                'model': '530i',
                'trim': 'xDrive',
                'odometer': 25000,
                'primary_damage': 'REAR END',
                'secondary_damage': 'MINOR DENT/SCRATCHES',
                'airbag': 'NOT DEPLOYED',
                'title': 'SALVAGE',
                'location': 'HOUSTON (TX)',
                'sale_date': '2024-03-15',
                'current_bid': 18500,
                'buy_now': 25000,
                'estimated_retail_value': 45000,
                'images_count': 24
            },
            {
                'lot_number': '87654321',
                'vin': 'WBA53CH05LCJ12345',
                'year': 2022,
                'make': 'BMW',
                'model': '540i',
                'trim': 'xDrive M Sport',
                'odometer': 15000,
                'primary_damage': 'SIDE',
                'secondary_damage': 'NONE',
                'airbag': 'NOT DEPLOYED',
                'title': 'SALVAGE',
                'location': 'LOS ANGELES (CA)',
                'sale_date': '2024-03-18',
                'current_bid': 28000,
                'buy_now': 35000,
                'estimated_retail_value': 62000,
                'images_count': 32
            }
        ]
    
    def filter_by_damage(self, vehicles: List[Dict]) -> List[Dict]:
        """
        Damage tipinə görə filtrlə
        """
        filtered = []
        
        for car in vehicles:
            # Front damage yoxdur
            if self.criteria['exclude_front_damage']:
                if 'FRONT' in car['primary_damage'].upper():
                    continue
            
            # Airbag açılmayıb
            if self.criteria['airbag_not_deployed']:
                if 'DEPLOYED' in car['airbag'].upper():
                    continue
            
            filtered.append(car)
        
        return filtered
    
    def check_vin_options(self, vin: str) -> Dict:
        """
        VIN-dən BMW opsiyalarını yoxla
        """
        print(f"\n🔍 VIN yoxlanılır: {vin}")
        
        # BMW VIN decoder (real API üçün)
        # Burada bimmer.work və ya başqa VIN decoder API istifadə olunmalı
        
        options = {
            'vin': vin,
            'driving_assistant_pro': False,  # 5AS option kodu
            'harman_kardon': False,          # 676 option kodu
            'bowers_wilkins': False,         # 688 option kodu
            'soft_close': False,             # 316 option kodu
            'comfort_access': True,          # 322 option kodu
            'parking_assistant': True        # 2VB option kodu
        }
        
        return options
    
    def calculate_total_cost(self, vehicle: Dict) -> Dict:
        """
        Ümumi xərc hesabla
        """
        # Copart fees (təxmini)
        vehicle_price = vehicle['current_bid']
        buyer_fee = vehicle_price * 0.10  # 10% buyer fee
        gate_fee = 79  # Gate fee
        title_fee = 75  # Title processing
        doc_fee = 50   # Documentation fee
        
        # Shipping (location-a görə)
        if 'CA' in vehicle['location']:
            shipping = 1500  # West Coast
        elif 'TX' in vehicle['location']:
            shipping = 1200  # Texas
        else:
            shipping = 1000  # Other
        
        # Təmir xərci (damage-ə görə təxmini)
        if 'REAR' in vehicle['primary_damage']:
            repair = 5000  # Rear end damage
        elif 'SIDE' in vehicle['primary_damage']:
            repair = 4000  # Side damage
        elif 'FRONT' in vehicle['primary_damage']:
            repair = 8000  # Front damage (worst)
        else:
            repair = 2000  # Minor
        
        total_cost = vehicle_price + buyer_fee + gate_fee + title_fee + doc_fee + shipping + repair
        
        return {
            'vehicle_price': vehicle_price,
            'buyer_fee': buyer_fee,
            'copart_fees': gate_fee + title_fee + doc_fee,
            'shipping': shipping,
            'estimated_repair': repair,
            'total_cost': total_cost,
            'retail_value': vehicle.get('estimated_retail_value', 0),
            'potential_profit': vehicle.get('estimated_retail_value', 0) - total_cost
        }
    
    def analyze_vehicle(self, vehicle: Dict) -> Dict:
        """
        Maşını tam təhlil et
        """
        # VIN opsiyalarını yoxla
        vin_options = self.check_vin_options(vehicle['vin'])
        
        # Xərc hesabla
        cost_breakdown = self.calculate_total_cost(vehicle)
        
        # Tövsiyə ver
        recommendation = self._generate_recommendation(vehicle, vin_options, cost_breakdown)
        
        return {
            'vehicle': vehicle,
            'options': vin_options,
            'costs': cost_breakdown,
            'recommendation': recommendation
        }
    
    def _generate_recommendation(self, vehicle: Dict, options: Dict, costs: Dict) -> Dict:
        """
        Alış tövsiyəsi ver
        """
        score = 0
        reasons = []
        
        # Yaş yoxla
        if vehicle['year'] >= 2022:
            score += 2
            reasons.append("✅ Yeni model (2022+)")
        
        # Damage yoxla
        if 'REAR' in vehicle['primary_damage']:
            score += 1
            reasons.append("✅ Arxa damage (asan təmir)")
        elif 'SIDE' in vehicle['primary_damage']:
            score += 1
            reasons.append("⚠️ Yan damage (orta səviyyə)")
        elif 'FRONT' in vehicle['primary_damage']:
            score -= 2
            reasons.append("❌ Ön damage (bahalı təmir)")
        
        # Airbag
        if 'NOT DEPLOYED' in vehicle['airbag']:
            score += 2
            reasons.append("✅ Hava yastığı açılmayıb")
        
        # Mileage
        if vehicle['odometer'] < 30000:
            score += 2
            reasons.append(f"✅ Az kilometr ({vehicle['odometer']} mil)")
        
        # Profit margin
        profit_margin = costs['potential_profit']
        if profit_margin > 10000:
            score += 3
            reasons.append(f"✅ Yaxşı profit margin (${profit_margin:,.0f})")
        elif profit_margin > 5000:
            score += 1
            reasons.append(f"⚠️ Orta profit margin (${profit_margin:,.0f})")
        else:
            score -= 1
            reasons.append(f"❌ Aşağı profit margin (${profit_margin:,.0f})")
        
        # Options yoxla
        if options.get('driving_assistant_pro'):
            score += 2
            reasons.append("✅ Driving Assistant Pro var")
        
        if options.get('harman_kardon') or options.get('bowers_wilkins'):
            score += 1
            reasons.append("✅ Premium audio var")
        
        # Qərar
        if score >= 8:
            decision = "🟢 ÇOX YAXŞI - ALMAĞA DƏYƏR!"
            max_bid = costs['vehicle_price'] * 1.15  # 15% daha çox
        elif score >= 5:
            decision = "🟡 YAXŞI - DİQQƏTLƏ BAX"
            max_bid = costs['vehicle_price'] * 1.05  # 5% daha çox
        else:
            decision = "🔴 KEÇ - ALMAĞA DƏYMƏZ"
            max_bid = 0
        
        return {
            'score': score,
            'decision': decision,
            'max_recommended_bid': max_bid,
            'reasons': reasons
        }
    
    def generate_report(self, analysis: Dict) -> str:
        """
        Təhlil hesabatı yarat
        """
        v = analysis['vehicle']
        o = analysis['options']
        c = analysis['costs']
        r = analysis['recommendation']
        
        report = f"""
{'='*80}
BMW {v['year']} {v['model']} - LOT #{v['lot_number']}
{'='*80}

📋 ƏSAS MƏLUMAT:
   VIN: {v['vin']}
   Model: {v['make']} {v['model']} {v['trim']}
   İl: {v['year']}
   Kilometr: {v['odometer']:,} mil
   Yerləşmə: {v['location']}
   Tender tarixi: {v['sale_date']}

💥 DAMAGE MƏLUMATI:
   Əsas damage: {v['primary_damage']}
   İkinci damage: {v['secondary_damage']}
   Hava yastığı: {v['airbag']}
   Title: {v['title']}

💰 QİYMƏT TƏHLILI:
   Cari tender: ${c['vehicle_price']:,.0f}
   Buyer fee: ${c['buyer_fee']:,.0f}
   Copart fees: ${c['copart_fees']:,.0f}
   Shipping: ${c['shipping']:,.0f}
   Təxmini təmir: ${c['estimated_repair']:,.0f}
   ──────────────────────
   ÜMUMİ XƏRC: ${c['total_cost']:,.0f}
   Retail dəyər: ${c['retail_value']:,.0f}
   Potensial qazanc: ${c['potential_profit']:,.0f}

🎯 TÖVSİYƏ: {r['decision']}
   Score: {r['score']}/10
   Maksimum tender: ${r['max_recommended_bid']:,.0f}

📝 SƏBƏBLƏR:
"""
        for reason in r['reasons']:
            report += f"   {reason}\n"
        
        report += f"\n{'='*80}\n"
        
        return report
    
    def run(self):
        """
        Əsas proqram
        """
        print("="*80)
        print("🚗 BMW G30 COPART FINDER")
        print("="*80)
        print("\n📋 AXTARIŞ KRİTERİYALARI:")
        print(f"   • Modellər: {', '.join(self.criteria['model'])}")
        print(f"   • İl aralığı: {self.criteria['year_min']}-{self.criteria['year_max']}")
        print(f"   • Ön damage yoxdur: {self.criteria['exclude_front_damage']}")
        print(f"   • Airbag açılmayıb: {self.criteria['airbag_not_deployed']}")
        print()
        
        # Maşınları tap
        vehicles = self.search_vehicles()
        
        # Filtrlə
        filtered = self.filter_by_damage(vehicles)
        print(f"\n✅ Filtrdən keçən: {len(filtered)} maşın")
        
        # Hər birini təhlil et
        print("\n" + "="*80)
        print("TƏHLIL NƏTİCƏLƏRİ")
        print("="*80)
        
        results = []
        for vehicle in filtered:
            analysis = self.analyze_vehicle(vehicle)
            results.append(analysis)
            
            # Hesabat yazdır
            report = self.generate_report(analysis)
            print(report)
        
        # Ən yaxşıları göstər
        print("\n" + "="*80)
        print("🏆 TOP TÖVSİYƏLƏR")
        print("="*80)
        
        # Score-a görə sort et
        results.sort(key=lambda x: x['recommendation']['score'], reverse=True)
        
        for i, analysis in enumerate(results[:3], 1):
            v = analysis['vehicle']
            r = analysis['recommendation']
            print(f"\n{i}. BMW {v['year']} {v['model']} - LOT #{v['lot_number']}")
            print(f"   {r['decision']}")
            print(f"   Score: {r['score']}/10")
            print(f"   Max bid: ${r['max_recommended_bid']:,.0f}")
        
        print("\n" + "="*80)
        print("✅ Axtarış tamamlandı!")
        print("="*80)


if __name__ == "__main__":
    finder = CopartBMWFinder()
    finder.run()
