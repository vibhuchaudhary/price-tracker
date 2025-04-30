import requests
from bs4 import BeautifulSoup

def scrape_flipkart_category(category):
    search_query = category.replace(' ', '%20')
    url = f"https://www.flipkart.com/search?q={search_query}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print("Failed to retrieve data")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')

    product_cards = soup.select('div.cPHDOP')  # Select all products

    results = []
    for card in product_cards:
        try:
            title = card.select_one('div.KzDlHZ')
            price = card.select_one('div.Nx9bqj._4b5DiR')
            link_tag = card.select_one('a.CGtC98')

            if title and price and link_tag:
                price_text = price.text.strip().replace('₹', '').replace(',', '')
                price_value = int(price_text)
                product = {
                    'title': title.text.strip(),
                    'price': price_value,
                    'link': "https://www.flipkart.com" + link_tag['href']
                }
                results.append(product)

        except Exception as e:
            print("Error parsing product:", e)

    return results

def main():
    category = input("Enter the category you want to search: ")
    products = scrape_flipkart_category(category)

    if not products:
        print("No products found.")
        return

    print(f"\nTotal {len(products)} products found for '{category}'.\n")

    # Ask how many results to display
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
        print(f"Link: {cheapest['link']}\n")

if __name__ == "__main__":
    main()