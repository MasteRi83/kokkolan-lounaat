import re
from datetime import datetime
from scrapers.base import RestaurantScraper


class LounaatInfoKokkolaScraper(RestaurantScraper):
    """Hakee Kokkolan ravintolan päivän ruokalistan suoraan Lounaat.info-koontisivulta."""
    def __init__(self, name, search_term, url, location, lunch_price, lunch_hours):
        super().__init__(name, url, location, lunch_price, lunch_hours)
        self.region = "kokkola"
        self.search_term = search_term.lower()
        self.lang_urls = {
            "fi": "https://lounaat.info",
            "en": "https://lounaat.info",
        }

    def parse_menu(self, soup, lang):
        for item in soup.select("div.item"):
            title_el = item.select_one("h3, .item-header a")
            if not title_el:
                continue
            title = title_el.get_text(" ", strip=True).lower()
            if self.search_term in title:
                dishes = []
                for li in item.select("li.menu-item, .dish, li, p.dish"):
                    txt = " ".join(li.get_text(" ", strip=True).split())
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

    def parse_menu(self, soup, lang):
        items = []
        for el in soup.select("p, li, span"):
            txt = " ".join(el.get_text(" ", strip=True).split())
            if any(k in txt.lower() for k in ["keitto", "salaatti", "lihapullat", "kastike", "perunat", "riisi", "broileri", "kala", "pata", "kiusaus", "mifu"]):
                if 6 < len(txt) < 110 and txt not in items:
                    items.append(txt)
        return items[:8] if items else self.menu_fallback[lang]


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
