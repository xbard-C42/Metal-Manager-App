"""
Gold Add-On API overrides (optional).
Provides a convenience function to fetch gold price.
"""
from api import fetch_price


def fetch_price_gold():
    """Fetch current gold price in USD."""
    return fetch_price("XAU")