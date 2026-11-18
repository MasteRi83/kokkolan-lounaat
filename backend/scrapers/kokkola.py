import re
from datetime import datetime
from scrapers.base import RestaurantScraper

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "fi-FI,fi;q=0.9,en;q=0.8",
}

DAYS_FI = ["Maanantai", "Tiistai", "Keskiviikko", "Torstai", "Perjantai"]
DAYS_SHORT = ["MA", "TI", "KE", "TO", "PE"]


def extract_day_lines(text, idx):
    today_full = DAYS_FI[idx]
    today_short = DAYS_SHORT[idx]
    next_full = DAYS_FI[idx + 1] if idx < 4 else "Lounas"
    next_short = DAYS_SHORT[idx + 1] if idx < 4 else "Lounas"

    patterns = [
        rf"{today_full}[^\n]*\n(.*?)(?:{next_full}|Lounas sis|Hinta|Allergeenit)",
        rf"\b{today_short}\b[^\n]*\n(.*?)(?:\b{next_short}\b|Lounas sis|Hinta)",
    ]
    for pat in patterns:
        match = re.search(pat, text, re.DOTALL | re.IGNORECASE)
        if match:
            lines = [
                " ".join(l.split())
                for l in match.group(1).split("\n")
                if len(l.strip()) > 3 and not re.match(r"^\d{1,2}\.\d{1,2}\.?$", l.strip())
            ]
            if lines:
                return lines[:8]
    return []


class HarjunRinkeliScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Harjun Rinkeli",
            "https://harjunleipomo.fi",
            "https://google.com",
            "11,00€ - 14,00€",
            "10:30 - 14:00",
        )
        self.region = "kokkola"
        self.headers = HEADERS

    def parse_menu(self, soup, lang):
        idx = datetime.now().weekday()
        if idx >= 5:
            return ["Ei lounasta viikonloppuna."]
        text = soup.get_text("\n", strip=True)
        section = text.split("Harjun Puffetti") if "Harjun Puffetti" in text else text
        lines = extract_day_lines(section, idx)
        return lines if lines else self.menu_fallback[lang]


class HarjunPuffettiScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Harjun Puffetti",
            "https://harjunleipomo.fi",
            "https://google.com",
            "10,00€ - 14,00€",
            "10:30 - 14:00",
        )
        self.region = "kokkola"
        self.headers = HEADERS

    def parse_menu(self, soup, lang):
        idx = datetime.now().weekday()
        if idx >= 5:
            return ["Ei lounasta viikonloppuna."]
        text = soup.get_text("\n", strip=True)
        section = text.split("Harjun Puffetti")[-1] if "Harjun Puffetti" in text else text
        lines = extract_day_lines(section, idx)
        return lines if lines else self.menu_fallback[lang]


class KulmaScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Kahvila-Ravintola Kulma",
            "https://lounastori.fi",
            "https://google.com",
            "13,30€",
            "10:45 - 14:00",
        )
        self.region = "kokkola"
        self.headers = HEADERS

    def parse_menu(self, soup, lang):
        idx = datetime.now().weekday()
        if idx >= 5:
            return ["Ei lounasta viikonloppuna."]
        text = soup.get_text("\n", strip=True)
        lines = extract_day_lines(text, idx)
        if lines:
            return lines
        food_words = ("keitto", "salaatti", "lihapullat", "kastike", "perunat", "riisi", "broileri", "kala", "pata", "kiusaus")
        fallback_lines = [
            " ".join(l.split())
            for l in text.split("\n")
            if any(w in l.lower() for w in food_words) and 6 < len(l.strip()) < 110
        ]
        return fallback_lines[:6] if fallback_lines else self.menu_fallback[lang]


class TowerBistroScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Tower Bistro",
            "https://lounastori.fi",
            "https://google.com",
            "15,90€",
            "10:30 - 14:00",
        )
        self.region = "kokkola"
        self.headers = HEADERS

    def parse_menu(self, soup, lang):
        idx = datetime.now().weekday()
        if idx >= 5:
            return ["Ei lounasta viikonloppuna."]
        text = soup.get_text("\n", strip=True)
        lines = extract_day_lines(text, idx)
        if lines:
            return lines
        food_words = ("keitto", "pihvi", "pasta", "lohi", "broileri", "possu", "nauta", "salaatti", "peruna", "riisi")
        fallback_lines = [
            " ".join(l.split())
            for l in text.split("\n")
            if any(w in l.lower() for w in food_words) and 6 < len(l.strip()) < 110
        ]
        return fallback_lines[:6] if fallback_lines else self.menu_fallback[lang]


class SataMaScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "100MA Social",
            "https://lounastori.fi",
            "https://google.com",
            "14,90€",
            "10:30 - 13:00",
        )
        self.region = "kokkola"
        self.headers = HEADERS

    def parse_menu(self, soup, lang):
        idx = datetime.now().weekday()
        if idx >= 5:
            return ["Ei lounasta viikonloppuna."]
        text = soup.get_text("\n", strip=True)
        lines = extract_day_lines(text, idx)
        if lines:
            return lines
        food_words = ("keitto", "pihvi", "pasta", "kala", "broileri", "possu", "nauta", "kasvis", "pata", "kääryleet")
        fallback_lines = [
            " ".join(l.split())
            for l in text.split("\n")
            if any(w in l.lower() for w in food_words) and 6 < len(l.strip()) < 110
        ]
        return fallback_lines[:6] if fallback_lines else self.menu_fallback[lang]


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
        self.headers = HEADERS

    def parse_menu(self, soup, lang):
        idx = datetime.now().weekday()
        if idx >= 5:
            return ["Ei lounasta viikonloppuna."]
        text = soup.get_text("\n", strip=True)
        lines = extract_day_lines(text, idx)
        if lines:
            return lines
        return [
            "Päivän lounaspöytä & vaihtuvat pizza-/pastavaihtoehdot (katso tarkka päivälista otsikon linkistä)"
        ]


class KungsKitchenScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Kung's Kitchen",
            "https://facebook.com",
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
