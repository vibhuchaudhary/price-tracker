import requests
from bs4 import BeautifulSoup
import logging

# Configure logging to display errors and warnings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def scrape_flipkart_category(category):
    """
    Scrapes product details from a Flipkart category search page.

    Args:
        category (str): The category to search for on Flipkart.

    Returns:
        list: A list of dictionaries, where each dictionary contains
              the title, price, and link of a product.
              Returns an empty list if scraping fails or no products are found.
    """

    # Prepare the search query and URL
    search_query = category.replace(' ', '%20')
    url = f"https://www.flipkart.com/search?q={search_query}"

    # Define headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:
        # Fetch the webpage content
        response = requests.get(url, headers=headers, timeout=10)  # Added timeout
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to retrieve data from Flipkart: {e}")
        return []  # Return an empty list in case of failure

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Select all product cards
    product_cards = soup.select('div.cPHDOP')

    results = []
    for card in product_cards:
        try:
            # Extract product details
            title = card.select_one('div.KzDlHZ')
            price = card.select_one('div.Nx9bqj._4b5DiR')
            link_tag = card.select_one('a.CGtC98')

            if title and price and link_tag:
                # Clean and convert the price
                price_text = price.text.strip().replace('₹', '').replace(',', '')
                try:
                    price_value = int(price_text)
                except ValueError:
                    logging.warning(f"Could not parse price: {price_text}. Skipping this product.")
                    continue  # Skip this product if price is invalid

                product = {
                    'title': title.text.strip(),
                    'price': price_value,
                    'link': "https://www.flipkart.com" + link_tag['href']  # Prepend base URL
                }
                results.append(product)

        except AttributeError as e:
            # Handle cases where elements are not found as expected
            logging.error(f"Error parsing product (AttributeError): {e}. HTML structure might have changed.")
        except Exception as e:
            # Handle any other unexpected exceptions during parsing
            logging.error(f"Error parsing product: {e}")

    return results


def main():
    """
    Main function to interactively search for products on Flipkart
    and display the results.
    """

    category = input("Enter the category you want to search: ").strip()
    products = scrape_flipkart_category(category)

    if not products:
        print("No products found.")
        return

    print(f"\nTotal {len(products)} products found for '{category}'.\n")

    # Ask how many results to display with proper error handling
    while True:
        try:
            count = int(input("How many top results do you want to see? "))
            if 0 < count <= len(products):
                break
            else:
                print(f"Please enter a number between 1 and {len(products)}")
        except ValueError:
            print("Please enter a valid number.")

    # Display selected number of products
    print("\nTop Products:\n")
    for idx, product in enumerate(products[:count], 1):
        print(f"{idx}. {product['title']} - ₹{product['price']}")
        print(f"   Link: {product['link']}\n")

    # Ask if user wants lowest price product
    choice = input("Do you want to see the lowest cost product on this page? (yes/no): ").strip().lower()
    if choice in ['yes', 'y']:
        cheapest = min(products, key=lambda x: x['price'])
        print("\n💸 Lowest Cost Product:")
        print(f"{cheapest['title']} - ₹{cheapest['price']}")
        print(f"Link: {cheapest['link']}")


if __name__ == "__main__":
    main()