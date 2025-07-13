import requests
from bs4 import BeautifulSoup
from decimal import Decimal
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

def parse_price(price_str):
    """Safely parse a price string to Decimal, return None if invalid."""
    try:
        cleaned = price_str.replace("£", "").replace("$", "").replace(",", "").strip()
        return Decimal(cleaned)
    except Exception:
        logger.warning(f"Failed to parse price: {price_str}")
        return None

def scrape_product_data(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to fetch product page for {url}: {e}")
        raise Exception("Could not fetch the product page. Please check the URL or your connection.") from e
    soup = BeautifulSoup(response.text, 'html.parser')
    domain = urlparse(url).netloc.lower()

    # Amazon
    if "amazon" in domain:
        name = soup.select_one("span#productTitle")
        price = soup.select_one("span.a-offscreen")
        if not name or not price:
            logger.warning(f"Amazon product info not found for {url}")
            raise Exception("amazon_not_supported")
        logger.info(f"Scraped Amazon product: {name.text.strip()} at {price.text.strip()}")
        return {
            "name": name.text.strip(),
            "current_price": parse_price(price.text.strip())
        }

    # Argos
    elif "argos" in domain:
        name = soup.select_one('span[data-test="product-title"]')
        price = soup.select_one('li[data-test="product-price-primary"] h2')
        if not name or not price:
            logger.warning(f"Argos product info not found for {url}")
            raise Exception("Could not find product info on Argos.")
        logger.info(f"Scraped Argos product: {name.text.strip()} at {price.text.strip()}")
        return {
            "name": name.text.strip(),
            "current_price": parse_price(price.text.strip())
        }

    # Nike
    elif "nike" in domain:
        name = soup.select_one('h1#pdp_product_title[data-testid="product_title"]')
        price = soup.select_one('span[data-testid="currentPrice-container"]')
        if not name or not price:
            logger.warning(f"Nike product info not found for {url}")
            raise Exception("Could not find product info on Nike.")
        logger.info(f"Scraped Nike product: {name.text.strip()} at {price.text.strip()}")
        return {
            "name": name.text.strip(),
            "current_price": parse_price(price.text.strip())
        }

    # Costco
    elif "costco" in domain:
        # Product name: <h1 class="product-name">
        name = soup.select_one("h1.product-name")
        # Product price: <span class="notranslate ng-star-inserted">
        price = soup.select_one("span.notranslate.ng-star-inserted")
        if not name or not price:
            logger.warning(f"Costco product info not found for {url}")
            raise Exception("Could not find product info on Costco.")
        logger.info(f"Scraped Costco product: {name.text.strip()} at {price.text.strip()}")
        return {
            "name": name.text.strip(),
            "current_price": parse_price(price.text.strip())
        }

    # TheWorks.co.uk
    elif "theworks.co.uk" in domain:
        # Product name: <h1 class="product-name">
        name = soup.select_one("h1.product-name")
        # Product price: <span class="value">
        price = soup.select_one("span.value")
        if not name or not price:
            logger.warning(f"TheWorks.co.uk product info not found for {url}")
            raise Exception("Could not find product info on TheWorks.co.uk.")
        logger.info(f"Scraped TheWorks.co.uk product: {name.text.strip()} at {price.text.strip()}")
        return {
            "name": name.text.strip(),
            "current_price": parse_price(price.text.strip())
        }

    # JDSports
    elif "jdsports" in domain:
        # Product name: <h1 data-e2e="product-name">
        name = soup.select_one('h1[data-e2e="product-name"]')
        # Product price: <span class="pri" data-e2e="product-price">
        price = soup.select_one('span.pri[data-e2e="product-price"]')
        if not name or not price:
            logger.warning(f"JDSports product info not found for {url}")
            raise Exception("Could not find product info on JDSports.")
        logger.info(f"Scraped JDSports product: {name.text.strip()} at {price.text.strip()}")
        return {
            "name": name.text.strip(),
            "current_price": parse_price(price.text.strip())
        }

    # Currys
    elif "currys" in domain:
        # Product name: <h1 class="product-name">
        name = soup.select_one("h1.product-name")
        # Product price: <span class="value">
        price = soup.select_one("span.value")
        if not name or not price:
            logger.warning(f"Currys product info not found for {url}")
            raise Exception("Could not find product info on Currys.")
        logger.info(f"Scraped Currys product: {name.text.strip()} at {price.text.strip()}")
        return {
            "name": name.text.strip(),
            "current_price": parse_price(price.text.strip())
        }

    # appliancecity
    elif "appliancecity" in domain:
        # Product name: <h1 class="product_title entry-title">
        name = soup.select_one("h1.product_title.entry-title")
        # Product price: <bdi>
        price = soup.select_one("bdi")
        if not name or not price:
            logger.warning(f"appliancecity product info not found for {url}")
            raise Exception("Could not find product info on appliancecity.")
        logger.info(f"Scraped appliancecity product: {name.text.strip()} at {price.text.strip()}")
        return {
            "name": name.text.strip(),
            "current_price": parse_price(price.text.strip())
        }
    
    # Atlantic Electrics
    elif "atlanticelectrics.co.uk" in domain:
        # Product name: <div class="product__title mobhide"><h1>...</h1></div>
        title_div = soup.select_one("div.product__title.mobhide h1")
        # Price: <span class="current-price product__price jsPrice">...</span>
        price_span = soup.select_one("span.current-price.product__price.jsPrice")
        if not title_div or not price_span:
            logger.warning(f"Atlantic Electrics product info not found for {url}")
            raise Exception("Could not find product info on Atlantic Electrics.")
        logger.info(f"Scraped Atlantic Electrics product: {title_div.text.strip()} at {price_span.text.strip()}")
        return {
            "name": title_div.text.strip(),
            "current_price": parse_price(price_span.text.strip())
        }

    # John Lewis
    elif "johnlewis.com" in domain:
        name = soup.select_one('h1[data-testid="product:title"]')
        price = soup.select_one('span[data-testid="price-now"]')
        if not name or not price:
            logger.warning(f"John Lewis product info not found for {url}")
            raise Exception("Could not find product info on John Lewis.")
        logger.info(f"Scraped John Lewis product: {name.text.strip()} at {price.text.strip()}")
        return {
            "name": name.text.strip(),
            "current_price": parse_price(price.text.strip())
        }

    # eBay
    elif "ebay." in domain:
        # Product name: <h1 class="x-item-title__mainTitle"><span class="ux-textspans ux-textspans--BOLD">...</span></h1>
        name = soup.select_one("h1.x-item-title__mainTitle span.ux-textspans--BOLD")
        # Price: <div class="x-price-primary" data-testid="x-price-primary"><span class="ux-textspans">£259.68</span></div>
        price = soup.select_one("div.x-price-primary span.ux-textspans")
        if not name or not price:
            logger.warning(f"eBay product info not found for {url}")
            raise Exception("Could not find product info on eBay.")
        logger.info(f"Scraped eBay product: {name.text.strip()} at {price.text.strip()}")
        return {
            "name": name.text.strip(),
            "current_price": parse_price(price.text.strip())
        }

    # Next
    elif "next.co.uk" in domain:
        # Product name: <h1 class="MuiTypography-root MuiTypography-h1 pdp-css-2w08za" data-testid="product-title">
        name = soup.select_one('h1[data-testid="product-title"]')
        # Product price: <span>£78</span> (first span containing £)
        price = soup.find("span", string=lambda text: text and "£" in text)
        if not name or not price:
            logger.warning(f"Next product info not found for {url}")
            raise Exception("Could not find product info on Next.")
        logger.info(f"Scraped Next product: {name.text.strip()} at {price.text.strip()}")
        return {
            "name": name.text.strip(),
            "current_price": parse_price(price.text.strip())
        }

    else:
        logger.warning(f"Unsupported site attempted: {url}")
        raise Exception("Sorry, this site is not supported yet.")