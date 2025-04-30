import requests
from bs4 import BeautifulSoup
import logging

# Configure logging to display errors and warnings
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_amazon_product(url):
    """
    Scrapes product details from an Amazon product page.

    Args:
        url (str): The URL of the Amazon product page.

    Returns:
        dict: A dictionary containing the scraped product details,
              or an error message if scraping fails.
    """

    # Define headers to mimic a browser request
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    # Initialize the result dictionary with default "not found" values
    result = {
        "url": url,
        "name": "Name not found",
        "price": "Price not found",
        "category": "Category not found",
        "availability": "Availability not found",
    }

    try:
        # Fetch the webpage content, with a timeout to prevent indefinite waiting
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "lxml")

        # Extract product name
        title_tag = soup.find("span", id="productTitle")
        result["name"] = title_tag.get_text(strip=True) if title_tag else result["name"]

        # Extract product price
        price_tag = soup.find("span", class_="a-offscreen")
        result["price"] = price_tag.get_text(strip=True) if price_tag else result["price"]

        # Extract availability information
        availability_tag = soup.find("div", id="availability")
        result["availability"] = availability_tag.get_text(strip=True) if availability_tag else result["availability"]

        # Extract category from breadcrumb navigation
        breadcrumb_tag = soup.find("div", id="wayfinding-breadcrumbs_feature_div")
        if breadcrumb_tag:
            category_links = breadcrumb_tag.find_all("a", class_="a-link-normal")
            categories = [a.get_text(strip=True) for a in category_links if a.get_text(strip=True)]
            result["category"] = " > ".join(categories) if categories else result["category"]

    except requests.exceptions.RequestException as e:
        # Handle exceptions related to HTTP requests (e.g., connection errors, timeouts)
        error_message = f"Failed to fetch page: {e}"
        logging.error(error_message)
        result["error"] = error_message
    except AttributeError as e:
        # Handle exceptions related to missing elements in the HTML (e.g., if Amazon changes its page structure)
        error_message = f"AttributeError while parsing: {e}. HTML structure might have changed."
        logging.error(error_message)
        result["error"] = error_message
    except Exception as e:
        # Handle any other unexpected exceptions
        error_message = f"An unexpected error occurred: {e}"
        logging.error(error_message)
        result["error"] = error_message

    return result


if __name__ == "__main__":
    # Example usage: Prompt the user for an Amazon product URL and scrape the data
    url = input("Enter Amazon product URL: ").strip()
    product_data = scrape_amazon_product(url)

    # Print the scraped data
    print("\n🟠 Amazon")
    print(f"Name        : {product_data.get('name', 'N/A')}")
    print(f"Price       : {product_data.get('price', 'N/A')}")
    print(f"Availability: {product_data.get('availability', 'N/A')}")
    print(f"Category    : {product_data.get('category', 'N/A')}")
    print(f"URL         : {product_data.get('url', 'N/A')}")
    if 'error' in product_data:
        print(f"Error       : {product_data['error']}")