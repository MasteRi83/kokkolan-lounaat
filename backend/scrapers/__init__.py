from scrapers.kokkola import (
    AmarilloScraper,
    HarjunPuffettiScraper,
    HarjunRinkeliScraper,
    KulmaScraper,
    KungsKitchenScraper,
    RossoScraper,
    SataMaScraper,
    TowerBistroScraper,
)


def get_all_scrapers():
    return {
        "kungs_kitchen": KungsKitchenScraper(),
        "tower_bistro": TowerBistroScraper(),
        "rosso": RossoScraper(),
        "amarillo": AmarilloScraper(),
        "100ma": SataMaScraper(),
        "harjun_puffetti": HarjunPuffettiScraper(),
        "harjun_rinkeli": HarjunRinkeliScraper(),
        "kulma": KulmaScraper(),
    }
