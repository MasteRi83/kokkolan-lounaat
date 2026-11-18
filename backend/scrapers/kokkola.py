import re
from datetime import datetime
from scrapers.base import RestaurantScraper

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "fi-FI,fi;q=0.9,en;q=0.8",
}

DAYS_FI = ["Maanantai", "Tiistai", "Keskiviikko", "Torstai", "Perjantai"]


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
        self.headers = HEADERS

    def parse_menu(self, soup, lang):
        idx = datetime.now().weekday()
        if idx >= 5:
            return ["Ei lounasta viikonloppuna."]
        today = DAYS_FI[idx]
        next_day = DAYS_FI[idx + 1] if idx < 4 else "Lounas tarjolla"

        text = soup.get_text("\n", strip=True)
        section = text.split("Harjun Rinkeli")[-1].split("Harjun Puffetti")[0] if "Harjun Rinkeli" in text else text
        match = re.search(rf"{today}\.?\s*\n(.*?){next_day}", section, re.DOTALL | re.IGNORECASE)
        if match:
            lines = [l.strip() for l in match.group(1).split("\n") if len(l.strip()) > 3]
            return lines[:6] if lines else self.menu_fallback[lang]
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
        self.headers = HEADERS

    def parse_menu(self, soup, lang):
        idx = datetime.now().weekday()
        if idx >= 5:
            return ["Ei lounasta viikonloppuna."]
        today = DAYS_FI[idx]
        next_day = DAYS_FI[idx + 1] if idx < 4 else "Lounas tarjolla"

        text = soup.get_text("\n", strip=True)
        section = text.split("Harjun Puffetti")[-1] if "Harjun Puffetti" in text else text
        match = re.search(rf"{today}\.?\s*\n(.*?){next_day}", section, re.DOTALL | re.IGNORECASE)
        if match:
            lines = [l.strip() for l in match.group(1).split("\n") if len(l.strip()) > 3]
            return lines[:6] if lines else self.menu_fallback[lang]
        return self.menu_fallback[lang]


class KulmaScraper(RestaurantScraper):
    def __init__(self):
        super().__init__(
            "Kahvila-Ravintola Kulma",
            "https://compass-group.fi",
            "https://google.com",
            "13,30€",
            "10:45 - 14:00",
        )
        self.region = "kokkola"
        self.headers = HEADERS
        self.lang_urls = {
            "fi": "https://compass-group.fi",
            "en": "https://compass-group.fi",
        }

    async def get_lunch_info(self, lang="fi", format="json"):
        return await super().get_lunch_info(lang=lang, format="json")

    def parse_json_menu(self, data, lang):
        today_iso = datetime.now().strftime("%Y-%m-%d")
        items = []
        for day_menu in data.get("MenusForDays", []):
            if today_iso in day_menu.get("Date", ""):
                for set_menu in day_menu.get("SetMenus", []):
                    comps = [c.strip() for c in set_menu.get("Components", []) if c.strip()]
                    if comps:
                        items.append(", ".join(comps))
                break
        return items if items else self.menu_fallback[lang]


class LounasMenuKokkolaScraper(RestaurantScraper):
    """Hakee listan Lounasmenu.fi Kokkola -sivulta (ei estä pilvipalvelimia)."""
    def __init__(self, name, search_term, url, location, lunch_price, lunch_hours):
        super().__init__(name, url, location, lunch_price, lunch_hours)
        self.region = "kokkola"
        self.headers = HEADERS
        self.search_term = search_term.lower()
        self.lang_urls = {
            "fi": "https://www.lounasmenu.fi/kokkola/",
            "en": "https://www.lounasmenu.fi/kokkola/",
        }

    def parse_menu(self, soup, lang):
        for card in soup.select("article, .restaurant-card, .menu-card, div"):
            heading = card.find(["h2", "h3", "h4"])
            if not heading:
                continue
            if self.search_term in heading.get_text(" ", strip=True).lower():
                dishes = []
                for row in card.select("li, p, .menu-item"):
                    txt = " ".join(row.get_text(" ", strip=True).split())
                    if 5 < len(txt) < 140 and self.search_term not in txt.lower() and "€" not in txt[:5]:
                        if txt not in dishes:
                            dishes.append(txt)
                if dishes:
                    return dishes[:8]
        return self.menu_fallback[lang]


class TowerBistroScraper(LounasMenuKokkolaScraper):
    def __init__(self):
        super().__init__(
            "Tower Bistro",
            "tower bistro",
            "https://towerbistro.fi/lounas/",
            "https://google.com",
            "15,90€",
            "10:30 - 14:00",
        )


class RossoScraper(LounasMenuKokkolaScraper):
    def __init__(self):
        super().__init__(
            "Rosso Kokkola",
            "rosso",
            "https://raflaamo.fi",
            "https://google.com",
            "13,70€ - 16,90€",
            "11:00 - 14:00",
        )


class SataMaScraper(LounasMenuKokkolaScraper):
    def __init__(self):
        super().__init__(
            "100MA Social",
            "100ma",
            "https://www.100masocial.fi/fi/menu",
            "https://google.com",
            "14,90€",
            "10:30 - 13:00",
        )


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
