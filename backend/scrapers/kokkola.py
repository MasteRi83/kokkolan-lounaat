import csv
import io
import logging
import httpx
from scrapers.base import RestaurantScraper

# VAIHDA TÄHÄN OMA JULKAISTU GOOGLE SHEETS CSV-OSOITTEESI:
# (Tiedosto -> Jaa -> Julkaise verkossa -> Taulukko1 -> Pilkuilla erotetut arvot .csv)
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSMAqZy7NbwtWM3Bu3Y6LE9HWoP0KlXzwjzldeNn1me6yMrkYN-zdypgPtYXxEaxGHSj8XGQD21iUsd/pub?gid=0&single=true&output=csv"

_SHEET_CACHE = None


async def load_sheet_rows():
    global _SHEET_CACHE
    if _SHEET_CACHE is not None:
        return _SHEET_CACHE

    if not SHEET_CSV_URL or "LIITA_TÄHÄN" in SHEET_CSV_URL:
        logging.error("SHEET_CSV_URL puuttuu kokkola.py -tiedostosta!")
        return {}

    try:
        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
            response = await client.get(SHEET_CSV_URL)
            response.raise_for_status()
            text = response.content.decode("utf-8")

        reader = csv.reader(io.StringIO(text))
        rows = list(reader)
        parsed = {}

        # Ohitetaan otsikkorivi (rivi 1) ja luetaan sarake A (nimi), B (url), C (menu)
        for row in rows[1:]:
            if len(row) >= 1 and row.strip():
                ravintola_nimi = row.strip().lower()
                ravintola_url = row.strip() if len(row) >= 2 else ""
                ruokalista_str = row.strip() if len(row) >= 3 else ""
                parsed[ravintola_nimi] = {
                    "url": ravintola_url,
                    "menu": ruokalista_str,
                }

        _SHEET_CACHE = parsed
        return parsed
    except Exception as e:
        logging.error(f"Virhe Google Sheets CSV:n latauksessa: {e!r}")
        return {}


class GoogleSheetKokkolaScraper(RestaurantScraper):
    def __init__(self, name, sheet_key, default_url, location, lunch_price, lunch_hours):
        super().__init__(name, default_url, location, lunch_price, lunch_hours)
        self.region = "kokkola"
        self.sheet_key = sheet_key.lower()

    async def get_lunch_info(self, lang="fi", format="html"):
        sheet_data = await load_sheet_rows()
        row = sheet_data.get(self.sheet_key)

        menu_lines = self.menu_fallback[lang]
        final_url = self.url

        if row:
            if row["url"]:
                final_url = row["url"]

            raw_menu = row["menu"]
            if raw_menu:
                # Pilkotaan Apps Scriptin " • "-erottimella yhdistetyt ruoat omiksi riveiksi
                parts = [part.strip() for part in raw_menu.split("•") if part.strip()]
                if parts:
                    menu_lines = parts

        return (
            self.discount[lang],
            self.is_student_cantine,
            self.location,
            self.lunch_hours,
            self.lunch_price,
            menu_lines,
            self.name,
            final_url,
        )


class KungsKitchenScraper(GoogleSheetKokkolaScraper):
    def __init__(self):
        super().__init__(
            name="Kung's Kitchen",
            sheet_key="Kung's Kitchen",
            default_url="https://lounaat.info",
            location="https://google.com",
            lunch_price="13,50€",
            lunch_hours="10:45 - 15:00",
        )


class TowerBistroScraper(GoogleSheetKokkolaScraper):
    def __init__(self):
        super().__init__(
            name="Tower Bistro",
            sheet_key="Tower Bistro",
            default_url="https://lounaat.info",
            location="https://google.com",
            lunch_price="15,90€",
            lunch_hours="10:30 - 14:00",
        )


class RossoScraper(GoogleSheetKokkolaScraper):
    def __init__(self):
        super().__init__(
            name="Rosso Kokkola",
            sheet_key="Rosso Kokkola",
            default_url="https://lounaat.info",
            location="https://google.com",
            lunch_price="13,70€ - 16,90€",
            lunch_hours="11:00 - 14:00",
        )


class SataMaScraper(GoogleSheetKokkolaScraper):
    def __init__(self):
        super().__init__(
            name="100MA Social",
            sheet_key="100MA Social",
            default_url="https://100masocial.fi",
            location="https://google.com",
            lunch_price="14,90€",
            lunch_hours="10:30 - 13:00",
        )


class HarjunPuffettiScraper(GoogleSheetKokkolaScraper):
    def __init__(self):
        super().__init__(
            name="Harjun Puffetti",
            sheet_key="Harjun Puffetti",
            default_url="https://lounaat.info",
            location="https://google.com",
            lunch_price="10,00€ - 14,00€",
            lunch_hours="10:30 - 14:00",
        )


class HarjunRinkeliScraper(GoogleSheetKokkolaScraper):
    def __init__(self):
        super().__init__(
            name="Harjun Rinkeli",
            sheet_key="Harjun Rinkeli",
            default_url="https://lounaat.info",
            location="https://google.com",
            lunch_price="11,00€ - 14,00€",
            lunch_hours="10:30 - 14:00",
        )


class KulmaScraper(GoogleSheetKokkolaScraper):
    def __init__(self):
        super().__init__(
            name="Kahvila-Ravintola Kulma",
            sheet_key="Kahvila-Ravintola Kulma",
            default_url="https://compass-group.fi",
            location="https://google.com",
            lunch_price="13,30€",
            lunch_hours="10:45 - 14:00",
        )
