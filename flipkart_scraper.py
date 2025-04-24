import ssl
import re
from urllib.request import Request, urlopen
from urllib.error   import HTTPError, URLError
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

    title_tag = soup.select_one("h1._6EBuvT span.VU-ZEz")
    name = title_tag.get_text(strip=True) if title_tag else "N/A"

    price_tag = soup.select_one("div.Nx9bqj.CxhGGd")
    price = price_tag.get_text(strip=True) if price_tag else "N/A"

    cat_tags = soup.select("a.R0cyWM")
    if cat_tags and len(cat_tags) > 1:
        category = " > ".join(tag.get_text(strip=True) for tag in cat_tags[1:])
    else:
        category = "N/A"

    return {
        "Product Name": name,
        "Price": price,
        "Category": category
    }
