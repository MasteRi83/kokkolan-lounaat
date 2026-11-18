import re
from datetime import datetime
from scrapers.base import RestaurantScraper


class TowerBistroScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Tower Bistro",
            "https://towerbistro.fi",
            "https://google.com",
            "15,90€",
            "10:30 - 14:00",
        )
        self.region = "kokkola"

    def parse_menu(self, soup, lang):
        days = ["Maanantai", "Tiistai", "Keskiviikko", "Torstai", "Perjantai"]
        idx = datetime.now().weekday()
        if idx >= 5:
            return ["Ei lounasta viikonloppuna."]
        today = days[idx]
        next_day = days[idx + 1] if idx < 4 else "Hinta"

        text = soup.get_text("\n", strip=True)
        pattern = re.compile(rf"{today}.*?\n(.*?)(?:{next_day}|Lounas sis|Alennukset)", re.DOTALL | re.IGNORECASE)
        match = pattern.search(text)
        if match:
            lines = [
                line.strip()
                for line in match.group(1).split("\n")
                if len(line.strip()) > 3 and not re.match(r"^\d{1,2}\.\d{1,2}\.?$", line.strip())
            ]
            return lines[:8] if lines else self.menu_fallback[lang]
        return self.menu_fallback[lang]


class HarjunPuffettiScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Harjun Puffetti",
            "https://harjunleipomo.fi/lounas",
            "https://google.com",
            "10,00€ - 14,00€",
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
        puffetti_part = text.split("Harjun Puffetti")[-1] if "Harjun Puffetti" in text else text
        pattern = re.compile(rf"{today}\.?\s*(.*?){next_day}", re.DOTALL | re.IGNORECASE)
        match = pattern.search(puffetti_part)
        if match:
            lines = [line.strip() for line in match.group(1).split("\n") if len(line.strip()) > 3]
            return lines[:6] if lines else self.menu_fallback[lang]
        return self.menu_fallback[lang]


class HarjunRinkeliScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Harjun Rinkeli",
            "https://harjunleipomo.fi/lounas",
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
        rinkeli_part = text.split("Harjun Puffetti")[0] if "Harjun Puffetti" in text else text
        pattern = re.compile(rf"{today}\.?\s*(.*?){next_day}", re.DOTALL | re.IGNORECASE)
        match = pattern.search(rinkeli_part)
        if match:
            lines = [line.strip() for line in match.group(1).split("\n") if len(line.strip()) > 3]
            return lines[:6] if lines else self.menu_fallback[lang]
        return self.menu_fallback[lang]


class RossoScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Rosso Kokkola",
            "https://raflaamo.fi",
            "https://google.com",
            "13,70€ - 16,90€",
            "11:00 - 14:00",
        )
        self.region = "kokkola"

    def parse_menu(self, soup, lang):
        days = ["Maanantai", "Tiistai", "Keskiviikko", "Torstai", "Perjantai"]
        idx = datetime.now().weekday()
        if idx >= 5:
            return ["Ei erillistä lounaslistaa viikonloppuna (à la carte)."]
        today = days[idx]
        next_day = days[idx + 1] if idx < 4 else "Viikon"

        text = soup.get_text("\n", strip=True)
        pattern = re.compile(rf"{today}.*?\n(.*?)(?:{next_day}|Päivän|Salaatti|Pizza|Allergeenit)", re.DOTALL | re.IGNORECASE)
        match = pattern.search(text)
        if match:
            lines = [line.strip() for line in match.group(1).split("\n") if len(line.strip()) > 3]
            return lines[:8] if lines else self.menu_fallback[lang]
        return self.menu_fallback[lang]


class KulmaScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Kahvila-Ravintola Kulma",
            "https://www.compass-group.fi/ravintolat-ja-ruokalistat/foodco/kaupungit/kokkola/kulma/",
            "https://google.com",
            "13,30€",
            "10:45 - 14:00",
        )
        self.region = "kokkola"

    def parse_menu(self, soup, lang):
        items = []
        for el in soup.select("p, li, span"):
            txt = " ".join(el.get_text(" ", strip=True).split())
            if any(k in txt.lower() for k in ["keitto", "salaatti", "lihapullat", "kastike", "perunat", "riisi", "broileri", "kala", "pata", "kiusaus", "mifu"]):
                if 6 < len(txt) < 110 and txt not in items:
                    items.append(txt)
        return items[:8] if items else self.menu_fallback[lang]


class SataMaScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "100MA Social",
            "https://www.100masocial.fi/fi/menu",
            "https://google.com",
            "14,90€",
            "10:30 - 13:00",
        )
        self.region = "kokkola"

    def parse_menu(self, soup, lang):
        days = ["Maanantai", "Tiistai", "Keskiviikko", "Torstai", "Perjantai"]
        idx = datetime.now().weekday()
        if idx >= 5:
            return ["Ei lounasta viikonloppuna."]
        today = days[idx]
        next_day = days[idx + 1] if idx < 4 else "Hinta"

        text = soup.get_text("\n", strip=True)
        pattern = re.compile(rf"{today}.*?\n(.*?)(?:{next_day}|Hinta|Varaa)", re.DOTALL | re.IGNORECASE)
        match = pattern.search(text)
        if match:
            lines = [line.strip() for line in match.group(1).split("\n") if len(line.strip()) > 3]
            return lines[:6] if lines else self.menu_fallback[lang]
        return self.menu_fallback[lang]


class KungsKitchenScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Kung's Kitchen",
            "https://www.facebook.com/KungsKitchen/",
            "https://google.com",
            "13,50€",
            "10:45 - 15:00",
        )
        self.region = "kokkola"

    def parse_menu(self, soup, lang):
        return [
            "Aasialainen lounasbuffet (kana-, nauta-, possu-, kala- ja kasvisvaihtoehdot)",
            "Sisältää kevätrullat, sushia, keiton, salaattipöydän sekä kahvin/teen",
        ]


class AmarilloScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Amarillo Kokkola",
            "https://raflaamo.fi",
            "https://google.com",
            "À la carte",
            "16:00 - 22:30",
        )
        self.region = "kokkola"

    def parse_menu(self, soup, lang):
        return ["Ei erillistä lounastarjoilua (avoinna arkisin klo 16 alkaen). Katso lista otsikon linkistä."]
