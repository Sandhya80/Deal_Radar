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
        image = soup.select_one("#imgTagWrapperId img")
        desc = soup.select_one("#productDescription p")
        if not name or not price:
            logger.warning(f"Amazon product info not found for {url}")
            raise Exception("amazon_not_supported")
        parsed_price = parse_price(price.text.strip())
        return {
            "name": name.text.strip(),
            "price": parsed_price,
            "current_price": parsed_price,
            "image_url": image['src'] if image and image.has_attr('src') else None,
            "description": desc.text.strip() if desc else ""
        }

    # Argos
    elif "argos" in domain:
        name = soup.select_one('span[data-test="product-title"]')
        price = soup.select_one('li[data-test="product-price-primary"] h2')
        image = soup.select_one('img[data-test="product-image"]')
        desc = soup.select_one('div[data-test="product-description"]')
        if not name or not price:
            logger.warning(f"Argos product info not found for {url}")
            raise Exception("Could not find product info on Argos.")
        parsed_price = parse_price(price.text.strip())
        return {
            "name": name.text.strip(),
            "price": parsed_price,
            "current_price": parsed_price,
            "image_url": image['src'] if image and image.has_attr('src') else None,
            "description": desc.text.strip() if desc else ""
        }

    # Nike
    elif "nike" in domain:
        name = soup.select_one('h1#pdp_product_title[data-testid="product_title"]')
        price = soup.select_one('span[data-testid="currentPrice-container"]')
        image = soup.select_one('img[data-testid="image-viewer-image"]')
        desc = soup.select_one('div[data-testid="product-description"]')
        if not name or not price:
            logger.warning(f"Nike product info not found for {url}")
            raise Exception("Could not find product info on Nike.")
        parsed_price = parse_price(price.text.strip())
        return {
            "name": name.text.strip(),
            "price": parsed_price,
            "current_price": parsed_price,
            "image_url": image['src'] if image and image.has_attr('src') else None,
            "description": desc.text.strip() if desc else ""
        }

    # Costco
    elif "costco" in domain:
        name = soup.select_one("h1.product-name")
        price = soup.select_one("span.notranslate.ng-star-inserted")
        image = soup.select_one("img.product-image")
        desc = soup.select_one("div.product-description")
        if not name or not price:
            logger.warning(f"Costco product info not found for {url}")
            raise Exception("Could not find product info on Costco.")
        parsed_price = parse_price(price.text.strip())
        return {
            "name": name.text.strip(),
            "price": parsed_price,
            "current_price": parsed_price,
            "image_url": image['src'] if image and image.has_attr('src') else None,
            "description": desc.text.strip() if desc else ""
        }

    # TheWorks.co.uk
    elif "theworks.co.uk" in domain:
        name = soup.select_one("h1.product-name")
        price = soup.select_one("span.value")
        image = soup.select_one("img.primary-image")
        desc = soup.select_one("div#product-description")
        if not name or not price:
            logger.warning(f"TheWorks.co.uk product info not found for {url}")
            raise Exception("Could not find product info on TheWorks.co.uk.")
        parsed_price = parse_price(price.text.strip())
        return {
            "name": name.text.strip(),
            "price": parsed_price,
            "current_price": parsed_price,
            "image_url": image['src'] if image and image.has_attr('src') else None,
            "description": desc.text.strip() if desc else ""
        }

    # JDSports
    elif "jdsports" in domain:
        name = soup.select_one('h1[data-e2e="product-name"]')
        price = soup.select_one('span.pri[data-e2e="product-price"]')
        image = soup.select_one('img[data-e2e="product-image"]')
        desc = soup.select_one('div[data-e2e="product-description"]')
        if not name or not price:
            logger.warning(f"JDSports product info not found for {url}")
            raise Exception("Could not find product info on JDSports.")
        parsed_price = parse_price(price.text.strip())
        return {
            "name": name.text.strip(),
            "price": parsed_price,
            "current_price": parsed_price,
            "image_url": image['src'] if image and image.has_attr('src') else None,
            "description": desc.text.strip() if desc else ""
        }

    # Currys
    elif "currys" in domain:
        name = soup.select_one("h1.product-name")
        price = soup.select_one("span.value")
        image = soup.select_one("img.primary-image")
        desc = soup.select_one("div#product-description")
        if not name or not price:
            logger.warning(f"Currys product info not found for {url}")
            raise Exception("Could not find product info on Currys.")
        parsed_price = parse_price(price.text.strip())
        return {
            "name": name.text.strip(),
            "price": parsed_price,
            "current_price": parsed_price,
            "image_url": image['src'] if image and image.has_attr('src') else None,
            "description": desc.text.strip() if desc else ""
        }

    # appliancecity
    elif "appliancecity" in domain:
        name = soup.select_one("h1.product_title.entry-title")
        price = soup.select_one("bdi")
        image = soup.select_one("img.attachment-woocommerce_thumbnail")
        desc = soup.select_one("div.woocommerce-product-details__short-description")
        if not name or not price:
            logger.warning(f"appliancecity product info not found for {url}")
            raise Exception("Could not find product info on appliancecity.")
        parsed_price = parse_price(price.text.strip())
        return {
            "name": name.text.strip(),
            "price": parsed_price,
            "current_price": parsed_price,
            "image_url": image['src'] if image and image.has_attr('src') else None,
            "description": desc.text.strip() if desc else ""
        }
    
    # Atlantic Electrics
    elif "atlanticelectrics.co.uk" in domain:
        title_div = soup.select_one("div.product__title.mobhide h1")
        price_span = soup.select_one("span.current-price.product__price.jsPrice")
        image = soup.select_one("img.product__image")
        desc = soup.select_one("div.product__description")
        if not title_div or not price_span:
            logger.warning(f"Atlantic Electrics product info not found for {url}")
            raise Exception("Could not find product info on Atlantic Electrics.")
        parsed_price = parse_price(price_span.text.strip())
        return {
            "name": title_div.text.strip(),
            "price": parsed_price,
            "current_price": parsed_price,
            "image_url": image['src'] if image and image.has_attr('src') else None,
            "description": desc.text.strip() if desc else ""
        }

    # John Lewis
    elif "johnlewis.com" in domain:
        name = soup.select_one('h1[data-testid="product:title"]')
        price = soup.select_one('span[data-testid="price-now"]')
        image = soup.select_one('img[data-testid="media-image"]')
        desc = soup.select_one('div[data-testid="product-description"]')
        if not name or not price:
            logger.warning(f"John Lewis product info not found for {url}")
            raise Exception("Could not find product info on John Lewis.")
        parsed_price = parse_price(price.text.strip())
        return {
            "name": name.text.strip(),
            "price": parsed_price,
            "current_price": parsed_price,
            "image_url": image['src'] if image and image.has_attr('src') else None,
            "description": desc.text.strip() if desc else ""
        }

    # eBay
    elif "ebay." in domain:
        name = soup.select_one("h1.x-item-title__mainTitle span.ux-textspans--BOLD")
        price = soup.select_one("div.x-price-primary span.ux-textspans")
        image = soup.select_one("img#icImg")
        desc = soup.select_one("div#viTabs_0_is")
        if not name or not price:
            logger.warning(f"eBay product info not found for {url}")
            raise Exception("Could not find product info on eBay.")
        parsed_price = parse_price(price.text.strip())
        return {
            "name": name.text.strip(),
            "price": parsed_price,
            "current_price": parsed_price,
            "image_url": image['src'] if image and image.has_attr('src') else None,
            "description": desc.text.strip() if desc else ""
        }

    # Next
    elif "next.co.uk" in domain:
        name = soup.select_one('h1[data-testid="product-title"]')
        price = soup.find("span", string=lambda text: text and "£" in text)
        image = soup.select_one('img[data-testid="product-image"]')
        desc = soup.select_one('div[data-testid="product-description"]')
        if not name or not price:
            logger.warning(f"Next product info not found for {url}")
            raise Exception("Could not find product info on Next.")
        parsed_price = parse_price(price.text.strip())
        return {
            "name": name.text.strip(),
            "price": parsed_price,
            "current_price": parsed_price,
            "image_url": image['src'] if image and image.has_attr('src') else None,
            "description": desc.text.strip() if desc else ""
        }

    else:
        logger.warning(f"Unsupported site attempted: {url}")
        raise Exception("Sorry, this site is not supported yet.")