from amazon_scraper import scrape_amazon_product
from flipkart_scraper import scrape_flipkart_product

def compare_prices():
    amazon_url = input("Enter Amazon product URL: ").strip()
    flipkart_url = input("Enter Flipkart product URL: ").strip()

    amazon_data = scrape_amazon_product(amazon_url)
    flipkart_data = scrape_flipkart_product(flipkart_url)

    print("\n========== PRICE COMPARISON ==========\n")

    if amazon_data:
        print("🟠 Amazon")
        print(f"Name        : {amazon_data['name']}")
        print(f"Price       : ₹{amazon_data['price']}" if amazon_data['price'] else "Price: Not available")
        print(f"Availability: {amazon_data['availability']}")
        print(f"URL         : {amazon_data['url']}\n")
    else:
        print("Amazon: ❌ Could not fetch product details.\n")

    if flipkart_data:
        print("🔵 Flipkart")
        print(f"Product Name: {flipkart_data['Product Name']}")
        print(f"Price       : {flipkart_data['Price']}")
        print(f"Category    : {flipkart_data['Category']}")
    else:
        print("Flipkart: ❌ Could not fetch product details.\n")


if __name__ == "__main__":
    compare_prices()
