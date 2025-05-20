import ssl
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


def scrape_flipkart_product(url):
    """
    Scrapes product details from a Flipkart product page.

    Args:
        url (str): The URL of the Flipkart product page.

    Returns:
        dict: A dictionary containing the scraped product details,
              or None if scraping fails.
    """

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
        with urlopen(req, context=ctx) as resp:
            soup = BeautifulSoup(resp.read(), "html.parser")
    except HTTPError as e:
        logging.error(f"HTTP Error: {e.code} for URL: {url}")
        return None
    except URLError as e:
        logging.error(f"Failed to reach server: {e.reason} for URL: {url}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred while fetching URL: {e} for URL: {url}")
        return None

    product_data = {} 
    try:
        title_tag = soup.select_one("h1._6EBuvT span.VU-ZEz")
        product_data["Product Name"] = title_tag.get_text(strip=True) if title_tag else "N/A"

        price_tag = soup.select_one("div.Nx9bqj.CxhGGd")
        product_data["Price"] = price_tag.get_text(strip=True) if price_tag else "N/A"

        discount_tag = soup.select_one("div.UkUFwK.WW8yVX span")
        product_data["Discount"] = discount_tag.get_text(strip=True) if discount_tag else "No discount"

        availability_tag = soup.select_one("div._2Jq5E4")
        product_data["Availability"] = availability_tag.get_text(strip=True) if availability_tag else "N/A"

        category_tag = soup.select_one("a._2whKao") 
        product_data["Category"] = category_tag.get_text(strip=True) if category_tag else "N/A"

    except AttributeError as e:
        logging.error(f"AttributeError while parsing Flipkart page: {e}. HTML structure might have changed for URL: {url}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred while parsing Flipkart page: {e} for URL: {url}")
        return None

    return product_data


if __name__ == "__main__":
    product_url = input("Enter Flipkart product URL: ").strip()
    if product_url:
        product_details = scrape_flipkart_product(product_url)
        if product_details:
            print("\n🔵 Flipkart Product Details:")
            for key, value in product_details.items():
                print(f"  {key}: {value}")
        else:
            print("Could not retrieve product details from Flipkart.")
    else:
        print("Please enter a valid Flipkart product URL.")
        