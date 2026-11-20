from scrapers.kokkola import (
    HarjunPuffettiScraper,
    HarjunRinkeliScraper,
    HickaroScraper,
    HildaScraper,
    KulmaScraper,
    KungsKitchenScraper,
    RossoScraper,
)


def get_all_scrapers():
    return {
        "kungs_kitchen": KungsKitchenScraper(),
        "rosso": RossoScraper(),
        "harjun_puffetti": HarjunPuffettiScraper(),
        "harjun_rinkeli": HarjunRinkeliScraper(),
        "kulma": KulmaScraper(),
        "hilda": HildaScraper(),
        "hickaro": HickaroScraper(),
    }
