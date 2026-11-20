from scrapers.kokkola import (
    HarjunPuffettiScraper,
    HarjunRinkeliScraper,
    HickaroScraper,
    HildaScraper,
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
        "100ma": SataMaScraper(),
        "harjun_puffetti": HarjunPuffettiScraper(),
        "harjun_rinkeli": HarjunRinkeliScraper(),
        "kulma": KulmaScraper(),
        "hilda": HildaScraper(),
        "hickaro": HickaroScraper(),
    }
