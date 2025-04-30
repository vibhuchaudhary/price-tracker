from scrapers.amazon_scraper import scrape_amazon_product
from scrapers.flipkart_scraper import scrape_flipkart_product
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def compare_prices():
    """
    Prompts the user for Amazon and Flipkart product URLs,
    scrapes the product details, and compares the prices.
    """

    amazon_url = input("Enter Amazon product URL: ").strip()
    flipkart_url = input("Enter Flipkart product URL: ").strip()

    try:
        amazon_data = scrape_amazon_product(amazon_url)
    except Exception as e:
        logging.error(f"Error scraping Amazon product: {e}")
        amazon_data = None  # Ensure amazon_data is None in case of an error

    try:
        flipkart_data = scrape_flipkart_product(flipkart_url)
    except Exception as e:
        logging.error(f"Error scraping Flipkart product: {e}")
        flipkart_data = None  # Ensure flipkart_data is None in case of an error

    print("\n========== PRICE COMPARISON ==========\n")

    if amazon_data:
        print("🟠 Amazon")
        print(f"Name        : {amazon_data.get('name', 'N/A')}")
        print(f"Price       : {amazon_data.get('price', 'N/A')}")
        print(f"Availability: {amazon_data.get('availability', 'N/A')}")
        print(f"URL         : {amazon_data.get('url', 'N/A')}\n")
    else:
        print("Amazon: ❌ Could not fetch product details.\n")

    if flipkart_data:
        print("🔵 Flipkart")
        print(f"Product Name: {flipkart_data.get('Product Name', 'N/A')}")
        print(f"Price       : {flipkart_data.get('Price', 'N/A')}")
        print(f"Category    : {flipkart_data.get('Category', 'N/A')}")
    else:
        print("Flipkart: ❌ Could not fetch product details.\n")


if __name__ == "__main__":
    compare_prices()