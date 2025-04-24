import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/116.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

def scrape_amazon_product(url):
    try:
        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")

        # Scraping product title
        name_tag = soup.select_one("#productTitle")
        
        # Scraping product price
        price_tag = soup.select_one(".a-price .a-offscreen")
        
        # Scraping product availability
        stock_tag = soup.select_one("#availability .a-declarative")
        
        # Scraping product category
        category_tag = soup.select_one(".a-list-item .a-link-normal")
        
        name = name_tag.get_text(strip=True) if name_tag else "N/A"
        price = float(price_tag.text.replace("₹", "").replace(",", "").strip()) if price_tag else None
        availability = stock_tag.get_text(strip=True) if stock_tag else "In Stock"
        category = category_tag.get_text(strip=True) if category_tag else "N/A"
        
        return {
            "name": name,
            "price": price,
            "availability": availability,
            "category": category,
            "url": url
        }
    except Exception as e:
        print(f"❌ Amazon scraping error: {e}")
        return None
