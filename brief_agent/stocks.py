"""Stock ticker database with popular stocks for autocomplete."""

# S&P 500 Top 50 + Nordic stocks
STOCK_TICKERS = [
    # US - S&P 500 Top companies
    {"ticker": "AAPL", "name": "Apple Inc.", "market": "NASDAQ"},
    {"ticker": "MSFT", "name": "Microsoft Corporation", "market": "NASDAQ"},
    {"ticker": "GOOGL", "name": "Alphabet Inc.", "market": "NASDAQ"},
    {"ticker": "AMZN", "name": "Amazon.com Inc.", "market": "NASDAQ"},
    {"ticker": "NVDA", "name": "NVIDIA Corporation", "market": "NASDAQ"},
    {"ticker": "META", "name": "Meta Platforms Inc.", "market": "NASDAQ"},
    {"ticker": "TSLA", "name": "Tesla Inc.", "market": "NASDAQ"},
    {"ticker": "BRK-B", "name": "Berkshire Hathaway", "market": "NYSE"},
    {"ticker": "JPM", "name": "JPMorgan Chase & Co.", "market": "NYSE"},
    {"ticker": "V", "name": "Visa Inc.", "market": "NYSE"},
    {"ticker": "JNJ", "name": "Johnson & Johnson", "market": "NYSE"},
    {"ticker": "WMT", "name": "Walmart Inc.", "market": "NYSE"},
    {"ticker": "MA", "name": "Mastercard Inc.", "market": "NYSE"},
    {"ticker": "PG", "name": "Procter & Gamble Co.", "market": "NYSE"},
    {"ticker": "HD", "name": "Home Depot Inc.", "market": "NYSE"},
    {"ticker": "XOM", "name": "Exxon Mobil Corp.", "market": "NYSE"},
    {"ticker": "BAC", "name": "Bank of America Corp.", "market": "NYSE"},
    {"ticker": "KO", "name": "Coca-Cola Co.", "market": "NYSE"},
    {"ticker": "PFE", "name": "Pfizer Inc.", "market": "NYSE"},
    {"ticker": "DIS", "name": "Walt Disney Co.", "market": "NYSE"},
    {"ticker": "NFLX", "name": "Netflix Inc.", "market": "NASDAQ"},
    {"ticker": "INTC", "name": "Intel Corporation", "market": "NASDAQ"},
    {"ticker": "AMD", "name": "Advanced Micro Devices", "market": "NASDAQ"},
    {"ticker": "CRM", "name": "Salesforce Inc.", "market": "NYSE"},
    {"ticker": "ADBE", "name": "Adobe Inc.", "market": "NASDAQ"},
    # Finnish stocks (Helsinki)
    {"ticker": "NOKIA.HE", "name": "Nokia Oyj", "market": "Helsinki"},
    {"ticker": "NDA-FI.HE", "name": "Nordea Bank Abp", "market": "Helsinki"},
    {"ticker": "FORTUM.HE", "name": "Fortum Oyj", "market": "Helsinki"},
    {"ticker": "SAMPO.HE", "name": "Sampo Oyj", "market": "Helsinki"},
    {"ticker": "NESTE.HE", "name": "Neste Oyj", "market": "Helsinki"},
    {"ticker": "UPM.HE", "name": "UPM-Kymmene Oyj", "market": "Helsinki"},
    {"ticker": "STERV.HE", "name": "Stora Enso Oyj", "market": "Helsinki"},
    {"ticker": "KNEBV.HE", "name": "Kone Oyj", "market": "Helsinki"},
    {"ticker": "ELISA.HE", "name": "Elisa Oyj", "market": "Helsinki"},
    {"ticker": "ORNBV.HE", "name": "Orion Oyj", "market": "Helsinki"},
    {"ticker": "METSB.HE", "name": "Metsä Board Oyj", "market": "Helsinki"},
    {"ticker": "KESKOB.HE", "name": "Kesko Oyj", "market": "Helsinki"},
    {"ticker": "WRT1V.HE", "name": "Wärtsilä Oyj", "market": "Helsinki"},
    {"ticker": "SOSI1.HE", "name": "Sotkamo Silver AB", "market": "Helsinki"},
    {"ticker": "QTCOM.HE", "name": "Qt Group Oyj", "market": "Helsinki"},
    {"ticker": "TELIA1.HE", "name": "Telia Company AB", "market": "Helsinki"},
    # Swedish stocks (Stockholm)
    {"ticker": "VOLV-B.ST", "name": "Volvo AB", "market": "Stockholm"},
    {"ticker": "ERIC-B.ST", "name": "Ericsson", "market": "Stockholm"},
    {"ticker": "HM-B.ST", "name": "H&M", "market": "Stockholm"},
    {"ticker": "SEB-A.ST", "name": "SEB AB", "market": "Stockholm"},
    {"ticker": "SWED-A.ST", "name": "Swedbank AB", "market": "Stockholm"},
    {"ticker": "ATCO-A.ST", "name": "Atlas Copco AB", "market": "Stockholm"},
    {"ticker": "SAND.ST", "name": "Sandvik AB", "market": "Stockholm"},
    {"ticker": "SPOT.ST", "name": "Spotify Technology", "market": "Stockholm"},
    # Norwegian stocks (Oslo)
    {"ticker": "EQNR.OL", "name": "Equinor ASA", "market": "Oslo"},
    {"ticker": "DNB.OL", "name": "DNB Bank ASA", "market": "Oslo"},
    {"ticker": "TEL.OL", "name": "Telenor ASA", "market": "Oslo"},
    {"ticker": "MOWI.OL", "name": "Mowi ASA", "market": "Oslo"},
    # Danish stocks (Copenhagen)
    {"ticker": "NOVO-B.CO", "name": "Novo Nordisk", "market": "Copenhagen"},
    {"ticker": "MAERSK-B.CO", "name": "A.P. Møller-Mærsk", "market": "Copenhagen"},
    {"ticker": "CARL-B.CO", "name": "Carlsberg A/S", "market": "Copenhagen"},
    {"ticker": "ORSTED.CO", "name": "Ørsted A/S", "market": "Copenhagen"},
]


def search_tickers(query: str, limit: int = 10) -> list[dict]:
    """
    Search for tickers matching a query.

    Args:
        query: Search string (matches ticker or company name)
        limit: Maximum number of results

    Returns:
        List of matching ticker dictionaries
    """
    if not query:
        return STOCK_TICKERS[:limit]

    query_lower = query.lower()
    matches = []

    for stock in STOCK_TICKERS:
        ticker_match = query_lower in stock["ticker"].lower()
        name_match = query_lower in stock["name"].lower()

        if ticker_match or name_match:
            # Prioritize exact ticker matches
            score = 0
            if stock["ticker"].lower().startswith(query_lower):
                score = 2
            elif ticker_match:
                score = 1
            matches.append((score, stock))

    # Sort by score (higher first), then by ticker name
    matches.sort(key=lambda x: (-x[0], x[1]["ticker"]))

    return [m[1] for m in matches[:limit]]
