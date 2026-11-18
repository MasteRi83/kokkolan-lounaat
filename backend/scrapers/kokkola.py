import re
from datetime import datetime
from scrapers.base import RestaurantScraper

BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "fi-FI,fi;q=0.9,en;q=0.8",
}


class KulmaScraper(RestaurantScraper):
    """Hakee Kulman listan suoraan Compass Groupin virallisesta JSON-rajapinnasta."""
    def __init__(self):
        super().__init__(
            "Kahvila-Ravintola Kulma",
            "https://compass-group.fi",
            "https://google.com",
            "13,30€",
            "10:45 - 14:00",
        )
        self.region = "kokkola"
        self.headers = BROWSER_HEADERS
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
                    name = set_menu.get("Name", "")
                    components = [c.strip() for c in set_menu.get("Components", []) if c.strip()]
                    if components:
                        prefix = f"{name}: " if name else ""
                        items.append(prefix + ", ".join(components))
                break
        return items if items else self.menu_fallback[lang]


class LounaatInfoKokkolaScraper(RestaurantScraper):
    """Hakee Kokkolan ravintolan listan Lounaat.info-sivulta selainotsakkeilla."""
    def __init__(self, name, search_term, url, location, lunch_price, lunch_hours):
        super().__init__(name, url, location, lunch_price, lunch_hours)
        self.region = "kokkola"
        self.headers = BROWSER_HEADERS
        self.search_term = search_term.lower()
        self.lang_urls = {
            "fi": "https://lounaat.info",
            "en": "https://lounaat.info",
        }

    def parse_menu(self, soup, lang):
        for item in soup.select("div.item"):
            header = item.select_one(".item-header")
            if not header:
                continue
            if self.search_term in header.get_text(" ", strip=True).lower():
                dishes = []
                for row in item.select("li, p.dish, .dish"):
                    txt = " ".join(row.get_text(" ", strip=True).split())
                    if txt and len(txt) > 3 and "lisää lounaslistaan" not in txt.lower():
                        dishes.append(txt)
                if not dishes:
                    body = item.select_one(".item-body")
                    if body:
                        for line in body.get_text("\n", strip=True).split("\n"):
                            clean = " ".join(line.split())
                            if len(clean) > 4 and self.search_term not in clean.lower():
                                dishes.append(clean)
                return dishes[:10] if dishes else self.menu_fallback[lang]
        return self.menu_fallback[lang]


class RossoScraper(LounaatInfoKokkolaScraper):
    def __init__(self):
        super().__init__(
            "Rosso Kokkola",
            "rosso",
            "https://raflaamo.fi",
            "https://google.com",
            "13,70€ - 16,90€",
            "11:00 - 14:00",
        )


class SataMaScraper(LounaatInfoKokkolaScraper):
    def __init__(self):
        super().__init__(
            "100MA Social",
            "100ma",
            "https://100masocial.fi",
            "https://google.com",
            "14,90€",
            "10:30 - 13:00",
        )


class HarjunPuffettiScraper(LounaatInfoKokkolaScraper):
    def __init__(self):
        super().__init__(
            "Harjun Puffetti",
            "puffetti",
            "https://harjunleipomo.fi",
            "https://google.com",
            "10,00€ - 14,00€",
            "10:30 - 14:00",
        )


class HarjunRinkeliScraper(LounaatInfoKokkolaScraper):
    def __init__(self):
        super().__init__(
            "Harjun Rinkeli",
            "rinkeli",
            "https://harjunleipomo.fi",
            "https://google.com",
            "11,00€ - 14,00€",
            "10:30 - 14:00",
        )


class TowerBistroScraper(LounaatInfoKokkolaScraper):
    def __init__(self):
        super().__init__(
            "Tower Bistro",
            "tower",
            "https://towerbistro.fi",
            "https://google.com",
            "15,90€",
            "10:30 - 14:00",
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
