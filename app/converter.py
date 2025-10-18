import requests
import os
import datetime
from dotenv import load_dotenv
from .db_rates import RateCache

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://v6.exchangerate-api.com/v6"


cache = RateCache()

def fetch_and_cache_rates(base_currency = "USD"):
    print("Fetching latest rates....")
    url = f"{BASE_URL}/{API_KEY}/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()

    if data.get("result") != "success":
        raise Exception("API fetch failed")
    
    rates = data["conversion_rates"]
    cache.save_rate(base_currency, rates)
    return rates

def get_rates():
    rates = cache.get_all_rates()
    if rates:
        print("Loaded rates from cache.")
        return rates
    return fetch_and_cache_rates()




# 1) try today's cache
# 2) fetch from API
# 3) fallback: try any older cached rates
# 4) nothing to fall back to — raise exception

def get_currencies(base_currency="USD"):

    if not API_KEY:
        raise RuntimeError("API_KEY not set. Put it in .env and load with load_dotenv().")

    try:
        rates = cache.get_all_rates()   # returns dict or None
        if rates:
            return sorted(rates.keys())
    except Exception:
        # log & continue to attempt a fetch; don't crash here
        import traceback; traceback.print_exc()

    try:
        url = f"{BASE_URL}/{API_KEY}/latest/{base_currency}"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        if data.get("result") != "success":
            raise RuntimeError(f"API error: {data}")

        rates = data.get("conversion_rates")
        if not rates:
            raise RuntimeError("API returned no conversion_rates field.")

        # cache and return
        cache.save_rates(base_currency, rates)
        return sorted(rates.keys())

    except Exception as e:
        try:
            old = cache.get_any_rates()
            if old:
                # warn but allow UI to work
                print("Warning: using stale/Old cached currency list due to API error:", str(e))
                return sorted(old.keys())
        except Exception:
            import traceback; traceback.print_exc()
    # If everything else fails.
        raise RuntimeError(f"Failed to load currencies: {e}")


def convert(amount, from_currency, to_currency):
    rates = get_rates()

    if from_currency not in rates or to_currency not in rates:
        raise ValueError("Unsupported currency")
    
    usd_amount = amount/rates[from_currency]
    converted = usd_amount * rates[to_currency]
    return round(converted, 2)

