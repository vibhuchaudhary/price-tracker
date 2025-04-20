from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)

def get_amazon_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        page = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(page.content, "html.parser")

        title = soup.find("span", id="productTitle")
        price = soup.find("span", class_="a-price-whole")
        rating = soup.find("span", class_="a-icon-alt")
        image = soup.find("img", id="landingImage")

        return {
            "source": "Amazon",
            "title": title.get_text(strip=True) if title else "Product Name Not Found",
            "price": price.get_text(strip=True) if price else "Price Not Found",
            "rating": rating.get_text(strip=True) if rating else "No Rating",
            "image": image["src"] if image else None
        }
    except Exception as e:
        print(f"Amazon Error: {e}")
        return {
            "source": "Amazon",
            "title": "Error loading product",
            "price": "Price Not Found",
            "rating": "No Rating",
            "image": None
        }

def get_flipkart_data(url):
    try:
        # Setup Chrome options
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # Setup ChromeDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        driver.get(url)
        time.sleep(3)  # Wait for page to load
        
        # If it's a search page, click the first product
        if "search?" in url:
            first_product = driver.find_element("css selector", "a._1fQZEK")
            first_product.click()
            time.sleep(3)
        
        # Now scrape the product page
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Updated selectors for Flipkart
        title = soup.find("span", class_="VU-ZEz")
        price = soup.find("div", class_="Nx9bqj CxhGGd")
        rating = soup.find("div", class_="XQDdHH")
        image = soup.find("img", class_="DByuf4 IZexXJ jLEJ7H")
        
        driver.quit()
        
        return {
            "source": "Flipkart",
            "title": title.get_text(strip=True) if title else "Product Name Not Found",
            "price": price.get_text(strip=True) if price else "Price Not Found",
            "rating": f"{rating.get_text(strip=True)}/5" if rating else "No Rating",
            "image": image["src"] if image else None
        }
    except Exception as e:
        print(f"Flipkart Error: {e}")
        return {
            "source": "Flipkart",
            "title": "Error loading product",
            "price": "Price Not Found",
            "rating": "No Rating",
            "image": None
        }

@app.route("/", methods=["GET", "POST"])
def index():
    products = []
    if request.method == "POST":
        urls = request.form.getlist("product_url")
        for url in urls:
            if "amazon" in url:
                products.append(get_amazon_data(url))
            elif "flipkart" in url:
                products.append(get_flipkart_data(url))
            else:
                products.append({
                    "source": "Unknown",
                    "title": "Invalid URL",
                    "price": "Price Not Found",
                    "rating": "No Rating",
                    "image": None
                })
    return render_template("index.html", products=products)

if __name__ == "__main__":
    app.run(debug=True)
