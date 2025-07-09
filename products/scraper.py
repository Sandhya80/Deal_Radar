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
        # Product name: <span id="productTitle" class="a-size-large celwidget">...</span>
        name = soup.select_one("span#productTitle")
        # Product price: <span class="a-price-whole"> or <span class="a-offscreen"> (for main price)
        price = soup.select_one("span.a-offscreen")
        if not name or not price:
            raise Exception("amazon_not_supported")
        return {
            "name": name.text.strip(),
            "current_price": Decimal(price.text.strip().replace("£", "").replace("$", "").replace(",", ""))
        }

    # Argos
    elif "argos" in domain:
        name = soup.select_one('span[data-test="product-title"]')
        price = soup.select_one('li[data-test="product-price-primary"] h2')
        if not name or not price:
            raise Exception("Could not find product info on Argos.")
        return {
            "name": name.text.strip(),
            "current_price": Decimal(price.text.strip().replace("£", "").replace(",", ""))
        }

    # Nike
    elif "nike" in domain:
        # Product name: <h1 id="pdp_product_title" data-testid="product_title">
        name = soup.select_one('h1#pdp_product_title[data-testid="product_title"]')
        # Product price: <span data-testid="currentPrice-container">
        price = soup.select_one('span[data-testid="currentPrice-container"]')
        if not name or not price:
            raise Exception("Could not find product info on Nike.")
        return {
            "name": name.text.strip(),
            "current_price": Decimal(price.text.strip().replace("£", "").replace("$", "").replace(",", ""))
        }

    # Costco
    elif "costco" in domain:
        # Product name: <h1 class="product-name">
        name = soup.select_one("h1.product-name")
        # Product price: <span class="notranslate ng-star-inserted">
        price = soup.select_one("span.notranslate.ng-star-inserted")
        if not name or not price:
            raise Exception("Could not find product info on Costco.")
        return {
            "name": name.text.strip(),
            "current_price": Decimal(price.text.strip().replace("£", "").replace("$", "").replace(",", ""))
        }

    # TheWorks.co.uk
    elif "theworks.co.uk" in domain:
        # Product name: <h1 class="product-name">
        name = soup.select_one("h1.product-name")
        # Product price: <span class="value">
        price = soup.select_one("span.value")
        if not name or not price:
            raise Exception("Could not find product info on TheWorks.co.uk.")
        return {
            "name": name.text.strip(),
            "current_price": Decimal(price.text.strip().replace("£", "").replace(",", ""))
        }

    # JDSports
    elif "jdsports" in domain:
        # Product name: <h1 data-e2e="product-name">
        name = soup.select_one('h1[data-e2e="product-name"]')
        # Product price: <span class="pri" data-e2e="product-price">
        price = soup.select_one('span.pri[data-e2e="product-price"]')
        if not name or not price:
            raise Exception("Could not find product info on JDSports.")
        return {
            "name": name.text.strip(),
            "current_price": Decimal(price.text.strip().replace("£", "").replace(",", ""))
        }

    # Currys
    elif "currys" in domain:
        # Product name: <h1 class="product-name">
        name = soup.select_one("h1.product-name")
        # Product price: <span class="value">
        price = soup.select_one("span.value")
        if not name or not price:
            raise Exception("Could not find product info on Currys.")
        return {
            "name": name.text.strip(),
            "current_price": Decimal(price.text.strip().replace("£", "").replace(",", ""))
        }

    # appliancecity
    elif "appliancecity" in domain:
        # Product name: <h1 class="product_title entry-title">
        name = soup.select_one("h1.product_title.entry-title")
        # Product price: <bdi>
        price = soup.select_one("bdi")
        if not name or not price:
            raise Exception("Could not find product info on appliancecity.")
        return {
            "name": name.text.strip(),
            "current_price": Decimal(price.text.strip().replace("£", "").replace(",", ""))
        }
    
    # Atlantic Electrics
    elif "atlanticelectrics.co.uk" in domain:
        # Product name: <div class="product__title mobhide"><h1>...</h1></div>
        title_div = soup.select_one("div.product__title.mobhide h1")
        # Price: <span class="current-price product__price jsPrice">...</span>
        price_span = soup.select_one("span.current-price.product__price.jsPrice")
        if not title_div or not price_span:
            raise Exception("Could not find product info on Atlantic Electrics.")
        return {
            "name": title_div.text.strip(),
            "current_price": Decimal(price_span.text.strip().replace("£", "").replace(",", ""))
        }

    # John Lewis
    elif "johnlewis.com" in domain:
        name = soup.select_one('h1[data-testid="product:title"]')
        price = soup.select_one('span[data-testid="price-now"]')
        if not name or not price:
            raise Exception("Could not find product info on John Lewis.")
        return {
            "name": name.text.strip(),
            "current_price": Decimal(price.text.strip().replace("£", "").replace(",", ""))
        }

    # eBay
    elif "ebay." in domain:
        # Product name: <h1 class="x-item-title__mainTitle"><span class="ux-textspans ux-textspans--BOLD">...</span></h1>
        name = soup.select_one("h1.x-item-title__mainTitle span.ux-textspans--BOLD")
        # Price: <div class="x-price-primary" data-testid="x-price-primary"><span class="ux-textspans">£259.68</span></div>
        price = soup.select_one("div.x-price-primary span.ux-textspans")
        if not name or not price:
            raise Exception("Could not find product info on eBay.")
        return {
            "name": name.text.strip(),
            "current_price": Decimal(price.text.strip().replace("£", "").replace(",", ""))
        }

    # Next
    elif "next.co.uk" in domain:
        # Product name: <h1 class="MuiTypography-root MuiTypography-h1 pdp-css-2w08za" data-testid="product-title">
        name = soup.select_one('h1[data-testid="product-title"]')
        # Product price: <span>£78</span> (first span containing £)
        price = soup.find("span", string=lambda text: text and "£" in text)
        if not name or not price:
            raise Exception("Could not find product info on Next.")
        return {
            "name": name.text.strip(),
            "current_price": Decimal(price.text.strip().replace("£", "").replace(",", ""))
        }

    else:
        raise Exception("Sorry, this site is not supported yet.")