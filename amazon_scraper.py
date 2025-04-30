import requests
from bs4 import BeautifulSoup

def scrape_amazon_product(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    result = {
        "url": url,
        "name": "Name not found",
        "price": "Price not found",
        "category": "Category not found",
        "availability": "Availability not found",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        result["error"] = f"Failed to fetch page: {e}"
        return result

    soup = BeautifulSoup(response.content, "lxml")

    # Name
    title_tag = soup.find("span", id="productTitle")
    if title_tag:
        result["name"] = title_tag.get_text(strip=True)

    # Price
    price_tag = soup.find("span", class_="a-offscreen")
    if price_tag:
        result["price"] = price_tag.get_text(strip=True)

    # Availability
    availability_tag = soup.find("div", id="availability")
    if availability_tag:
        result["availability"] = availability_tag.get_text(strip=True)

    # Category (new logic: from breadcrumb nav)
    breadcrumb_tag = soup.find("div", id="wayfinding-breadcrumbs_feature_div")
    if breadcrumb_tag:
        category_links = breadcrumb_tag.find_all("a", class_="a-link-normal")
        categories = [a.get_text(strip=True) for a in category_links if a.get_text(strip=True)]
        if categories:
            result["category"] = " > ".join(categories)

    return result

# Example usage
if __name__ == "__main__":
    url = input("Enter Amazon product URL: ").strip()
    data = scrape_amazon_product(url)

    print("\n🟠 Amazon")
    print(f"Name        : {data['name']}")
    print(f"Price       : {data['price']}")
    print(f"Availability: {data['availability']}")
    print(f"Category    : {data['category']}")
    print(f"URL         : {data['url']}")
    if 'error' in data:
        print(f"Error       : {data['error']}")
