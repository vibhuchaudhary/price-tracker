import ssl
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup

def scrape_flipkart_product(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
    }
    req = Request(url, headers=headers)

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        resp = urlopen(req, context=ctx)
    except HTTPError as e:
        print(f"HTTP Error: {e.code}")
        return
    except URLError as e:
        print(f"Failed to reach server: {e.reason}")
        return

    soup = BeautifulSoup(resp.read(), "html.parser")

    # Get product name
    title_tag = soup.select_one("h1._6EBuvT span.VU-ZEz")
    name = title_tag.get_text(strip=True) if title_tag else "N/A"

    # Get product price
    price_tag = soup.select_one("div.Nx9bqj.CxhGGd")
    price = price_tag.get_text(strip=True) if price_tag else "N/A"

    # Get discount information (e.g., 11% off)
    discount_tag = soup.select_one("div.UkUFwK.WW8yVX span")
    discount = discount_tag.get_text(strip=True) if discount_tag else "No discount"
    
    # Get product availability (checking for text like 'In stock' or 'Out of stock')
    availability_tag = soup.select_one("div._2Jq5E4")
    availability = availability_tag.get_text(strip=True) if availability_tag else "Availability info not available"

    # Return the desired format to match the Amazon scraper's output
    return {
        "name": name,
        "price": price,
        "discount": discount,
        "availability": availability,
        "url": url  # Pass the URL so the Flask app can link to the product page
    }
