import requests
from bs4 import BeautifulSoup
from decimal import Decimal
from urllib.parse import urlparse

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

def scrape_product_data(url):
    response = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')
    domain = urlparse(url).netloc.lower()

    # Amazon
    if "amazon" in domain:
        name = soup.select_one("#productTitle")
        price = soup.select_one(".a-price .a-offscreen")
        if not price:
            price = soup.select_one("#priceblock_ourprice")
        if not price:
            price = soup.select_one("#priceblock_dealprice")
        if not name or not price:
            raise Exception("amazon_not_supported")
        return {
            "name": name.text.strip(),
            "current_price": Decimal(price.text.strip().replace("£", "").replace("$", "").replace(",", ""))
        }

    # Argos
    elif "argos" in domain:
        name = soup.select_one('h1[data-test="product-title"]')
        price = soup.select_one('div[data-test="product-price"]')
        if not name or not price:
            raise Exception("Could not find product info on Argos.")
        return {
            "name": name.text.strip(),
            "current_price": Decimal(price.text.strip().replace("£", "").replace(",", ""))
        }

    # Nike
    elif "nike" in domain:
        name = soup.select_one("h1.headline")
        price = soup.select_one("div[data-test='product-price'] span")
        if not name or not price:
            raise Exception("Could not find product info on Nike.")
        return {
            "name": name.text.strip(),
            "current_price": Decimal(price.text.strip().replace("£", "").replace("$", "").replace(",", ""))
        }

    # Costco
    elif "costco" in domain:
        name = soup.select_one("h1.product-title")
        price = soup.select_one("div.product-price span.value")
        if not name or not price:
            raise Exception("Could not find product info on Costco.")
        return {
            "name": name.text.strip(),
            "current_price": Decimal(price.text.strip().replace("£", "").replace("$", "").replace(",", ""))
        }

    # TheWorks.co.uk
    elif "theworks.co.uk" in domain:
        name = soup.select_one("h1.product-title")
        price = soup.select_one("span.price")
        if not name or not price:
            raise Exception("Could not find product info on TheWorks.co.uk.")
        return {
            "name": name.text.strip(),
            "current_price": Decimal(price.text.strip().replace("£", "").replace(",", ""))
        }

    # JDSports
    elif "jdsports" in domain:
        name = soup.select_one("h1.product-title")
        price = soup.select_one("span.product-sales-price")
        if not name or not price:
            raise Exception("Could not find product info on JDSports.")
        return {
            "name": name.text.strip(),
            "current_price": Decimal(price.text.strip().replace("£", "").replace(",", ""))
        }

    # Currys
    elif "currys" in domain:
        name = soup.select_one("h1.product-title")
        price = soup.select_one("div.product-price span")
        if not name or not price:
            raise Exception("Could not find product info on Currys.")
        return {
            "name": name.text.strip(),
            "current_price": Decimal(price.text.strip().replace("£", "").replace(",", ""))
        }

    # HomeAppliances
    elif "homeappliances" in domain:
        name = soup.select_one("h1.product-title")
        price = soup.select_one("span.price")
        if not name or not price:
            raise Exception("Could not find product info on HomeAppliances.")
        return {
            "name": name.text.strip(),
            "current_price": Decimal(price.text.strip().replace("£", "").replace(",", ""))
        }

    # KitchenWorld
    elif "kitchenworld" in domain:
        name = soup.select_one("h1.product-title")
        price = soup.select_one("span.price")
        if not name or not price:
            raise Exception("Could not find product info on KitchenWorld.")
        return {
            "name": name.text.strip(),
            "current_price": Decimal(price.text.strip().replace("£", "").replace(",", ""))
        }

    else:
        raise Exception("Sorry, this site is not supported yet.")