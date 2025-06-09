import requests
from config import load_config

SYMBOLS = {'copper':'XCU'}  # extend via plugins

def fetch_price(symbol):
    cfg = load_config()
    api_key = cfg.get('api_key')
    if not api_key:
        raise RuntimeError("API key not set in config.json or SIM")
    url = 'https://api.metals-api.com/v1/latest'
    params = {'access_key': api_key, 'symbols': symbol, 'base': 'USD'}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()['rates'][symbol]


def fetch_metal_price(metal):
    symbol = SYMBOLS.get(metal)
    if not symbol:
        raise ValueError(f"Unsupported metal: {metal}")
    return fetch_price(symbol)