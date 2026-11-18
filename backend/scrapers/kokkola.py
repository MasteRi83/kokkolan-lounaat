import re
from datetime import datetime
from scrapers.base import RestaurantScraper


class LounaatInfoScraper(RestaurantScraper):
    """Yleishakija Lounaat.info-sivujen Kokkolan ravintoloille."""
    def __init__(self, name, url, location, lunch_price, lunch_hours):
        super().__init__(name, url, location, lunch_price, lunch_hours)
        self.region = "kokkola"

    def parse_menu(self, soup, lang):
        today_num = datetime.now().strftime("%-d.%-m.")
        day_names = ["maanantai", "tiistai", "keskiviikko", "torstai", "perjantai", "lauantai", "sunnuntai"]
        today_name = day_names[datetime.now().weekday()]
        
        menu_items = []
        for item in soup.select(".item"):
            header = item.select_one(".item-header")
            if not header:
                continue
            header_text = header.get_text(" ", strip=True).lower()
            if today_num in header_text or today_name in header_text:
                for dish in item.select(".menu-item, li, p"):
                    txt = " ".join(dish.get_text(" ", strip=True).split())
                    if txt and len(txt) > 3 and today_name not in txt.lower():
                        menu_items.append(txt)
                break
        return menu_items if menu_items else self.menu_fallback[lang]


class TowerBistroScraper(LounaatInfoScraper):
    def __init__(self):
        super().__init__(
            "Tower Bistro",
            "https://lounaat.info",
            "https://google.com",
            "15,90€",
            "10:30 - 14:00",
        )


class RossoScraper(LounaatInfoScraper):
    def __init__(self):
        super().__init__(
            "Rosso Kokkola",
            "https://lounaat.info",
            "https://google.com",
            "14,00€ - 16,90€",
            "11:00 - 14:00",
        )


class HarjunPuffettiScraper(LounaatInfoScraper):
    def __init__(self):
        super().__init__(
            "Harjun Puffetti",
            "https://lounaat.info",
            "https://google.com",
            "10,00€ - 14,00€",
            "10:30 - 14:00",
        )


class HarjunRinkeliScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Harjun Rinkeli",
            "https://harjunrinkeli.fi",
            "https://google.com",
            "11,00€ - 14,00€",
            "10:30 - 14:00",
        )
        self.region = "kokkola"

    def parse_menu(self, soup, lang):
        days = ["Maanantai", "Tiistai", "Keskiviikko", "Torstai", "Perjantai"]
        idx = datetime.now().weekday()
        if idx >= 5:
            return ["Ei lounasta viikonloppuna."]
        today = days[idx]
        next_day = days[idx + 1] if idx < 4 else "Lounas tarjolla"
        
        text = soup.get_text("\n", strip=True)
        pattern = re.compile(rf"{today}(.*?){next_day}", re.DOTALL | re.IGNORECASE)
        match = pattern.search(text)
        if match:
            lines = [line.strip() for line in match.group(1).split("\n") if len(line.strip()) > 3]
            return lines if lines else self.menu_fallback[lang]
        return self.menu_fallback[lang]


class KulmaScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Kahvila-Ravintola Kulma",
            "https://lounastori.fi/fi/page/67b85f0c4534cd043dd709bc",
            "https://google.com",
            "13,60€",
            "10:45 - 14:00",
        )
        self.region = "kokkola"

    def parse_menu(self, soup, lang):
        items = []
        for el in soup.select("p, li"):
            txt = " ".join(el.get_text(" ", strip=True).split())
            if any(k in txt.lower() for k in ["keitto", "salaatti", "lihapullat", "kastike", "perunat", "riisi", "broileri", "kala", "pata", "kiusaus"]):
                if len(txt) < 120:
                    items.append(txt)
        return items[:8] if items else self.menu_fallback[lang]


class SataMaScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "100MA Social",
            "https://lounastori.fi/fi/page/681db04d385bb1058bdc3fb3",
            "https://google.com",
            "14,90€",
            "10:30 - 13:00",
        )
        self.region = "kokkola"

    def parse_menu(self, soup, lang):
        items = []
        for el in soup.select("p, li"):
            txt = " ".join(el.get_text(" ", strip=True).split())
            if any(k in txt.lower() for k in ["keitto", "pata", "kääryleet", "kala", "broileri", "possu", "nauta", "kasvis"]):
                if len(txt) < 120:
                    items.append(txt)
        return items[:6] if items else self.menu_fallback[lang]


class KungsKitchenScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Kung's Kitchen",
            "https://lounastori.fi",
            "https://google.com",
            "13,50€",
            "10:45 - 15:00",
        )
        self.region = "kokkola"

    def parse_menu(self, soup, lang):
        return [
            "Aasialainen lounasbuffet & päivän vaihtuvat pääruoat (kana, nauta, possu, tofu/kasvis)",
            "Sisältää kevätrullat, sushia, keiton, salaattipöydän sekä kahvin/teen",
        ]


class AmarilloScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Amarillo Kokkola",
            "https://www.raflaamo.fi/fi/ravintola/kokkola/amarillo-kokkola/menu/14262/ruokalista",
            "https://google.com",
            "À la carte",
            "16:00 - 22:30",
        )
        self.region = "kokkola"

    def parse_menu(self, soup, lang):
        return ["Ei erillistä lounastarjoilua (avoinna arkisin klo 16 alkaen). Katso à la carte -lista linkistä."]
