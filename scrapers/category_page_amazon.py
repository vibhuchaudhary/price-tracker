import requests
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def scrape_amazon_category(search_keyword):
    """
    Retrieves all organic product listings from an Amazon search results page
    based on the search keyword and then identifies the entry with the lowest price.

    Args:
        search_keyword (str): The keyword to search for on Amazon.

    Returns:
        tuple: A tuple containing two elements:
            - list: A list of dictionaries, where each dictionary contains
                    the title, price, and link of all retrieved organic products.
                    Returns an empty list if scraping fails or no results are found.
            - dict: A dictionary representing the product with the lowest price,
                    or None if no products were found.
    """
    base_url = 'https://www.amazon.in/s?k='
    search_url = base_url + search_keyword.replace(' ', '+')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')
        listings = soup.find_all('div', {'data-component-type': 's-search-result'})
        all_products = []

        for listing in listings:
            # Skip sponsored products
            if listing.find('span', class_='sponsored-label-text'):
                continue

            title_element = listing.select_one('.a-size-medium.a-spacing-none.a-color-base.a-text-normal span')
            price_whole_element = listing.select_one('.a-price[data-a-size="xl"] .a-price-whole')
            price_fraction_element = listing.select_one('.a-price[data-a-size="xl"] .a-price-fraction')
            link_element = listing.select_one('a.a-link-normal.s-no-outline')

            title = title_element.text.strip() if title_element else None
            price_whole = price_whole_element.text.strip() if price_whole_element else None
            price_fraction = price_fraction_element.text.strip() if price_fraction_element else '00'
            link = 'https://www.amazon.in' + link_element['href'] if link_element and 'href' in link_element.attrs else None

            if title and price_whole and link:
                price_str = f"{price_whole}.{price_fraction}"
                try:
                    price_value = float(price_str.replace(',', ''))  # Remove comma if present
                    product = {
                        'title': title,
                        'price': price_str,
                        'price_value': price_value,  # Store numerical price for comparison
                        'link': link
                    }
                    all_products.append(product)
                except ValueError:
                    logging.warning(f"Could not parse price: {price_str} for '{title}'. Skipping price comparison for this item.")
                    product = {
                        'title': title,
                        'price': price_str,
                        'price_value': float('inf'),  # Assign infinity for comparison
                        'link': link
                    }
                    all_products.append(product)
            elif title and link:
                # If price is not available, still add the product with a default price_value
                product = {
                    'title': title,
                    'price': 'N/A',
                    'price_value': float('inf'),  # Ensure it doesn't affect lowest price
                    'link': link
                }
                all_products.append(product)

        lowest_price_product = None
        if all_products:
            try:
                lowest_price_product = min(all_products, key=lambda item: item['price_value'])
            except ValueError:
                logging.warning("Could not determine the lowest price among the entries.")

        return all_products, lowest_price_product

    except requests.exceptions.RequestException as e:
        logging.error(f"Error during request: {e}")
        return [], None
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return [], None


if __name__ == '__main__':
    search_term = input("Enter search keywords: ")

    all_entries, lowest_price_entry = scrape_amazon_category(search_term)

    if all_entries:
        print(f"\nAll organic Amazon products for '{search_term}':")
        for i, item in enumerate(all_entries):
            print(f"--- Entry {i + 1} ---")
            print(f"  Title: {item['title']}")
            print(f"  Price: ₹{item['price']}")
            print(f"  Link: {item['link']}")
        print("-" * 30)

        if lowest_price_entry:
            print("\nEntry with the lowest price:")
            print(f"  Title: {lowest_price_entry['title']}")
            print(f"  Price: ₹{lowest_price_entry['price']}")
            print(f"  Link: {lowest_price_entry['link']}")
        else:
            print("Could not determine the lowest price among the entries.")
    else:
        print("No organic products found or an error occurred.")