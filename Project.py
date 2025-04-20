from flask import Flask, jsonify, render_template, request
from models import init_db, save_price, get_price_history
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
init_db()

def get_amazon_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0",
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
            "url": url,
            "title": title.get_text(strip=True) if title else "Product Name Not Found",
            "price": price.get_text(strip=True) if price else "0",
            "rating": rating.get_text(strip=True) if rating else "No Rating",
            "image": image["src"] if image else None
        }
    except Exception as e:
        print(f"Amazon Error: {e}")
        return {
            "source": "Amazon",
            "url": url,
            "title": "Error loading product",
            "price": "0",
            "rating": "No Rating",
            "image": None
        }

def get_flipkart_data(url):
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get(url)
        time.sleep(3)

        if "search?" in url:
            first_product = driver.find_element("css selector", "a._1fQZEK")
            first_product.click()
            time.sleep(3)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        title = soup.find("span", class_="VU-ZEz")
        price = soup.find("div", class_="Nx9bqj CxhGGd")
        rating = soup.find("div", class_="XQDdHH")
        image = soup.find("img", class_="DByuf4 IZexXJ jLEJ7H")

        driver.quit()

        return {
            "source": "Flipkart",
            "url": url,
            "title": title.get_text(strip=True) if title else "Product Name Not Found",
            "price": price.get_text(strip=True) if price else "0",
            "rating": f"{rating.get_text(strip=True)}/5" if rating else "No Rating",
            "image": image["src"] if image else None
        }
    except Exception as e:
        print(f"Flipkart Error: {e}")
        return {
            "source": "Flipkart",
            "url": url,
            "title": "Error loading product",
            "price": "0",
            "rating": "No Rating",
            "image": None
        }


@app.route("/", methods=["GET", "POST"])
def index():
    products = []
    history_dates, history_prices = [], []

    if request.method == "POST":
        urls = request.form.getlist("product_url")
        for url in urls:
            if "amazon" in url:
                product = get_amazon_data(url)
            elif "flipkart" in url:
                product = get_flipkart_data(url)
            else:
                continue

            try:
                clean_price = int("".join(filter(str.isdigit, product["price"])))
                save_price(url, product["title"], clean_price, product["source"])
                history_dates, history_prices = get_price_history(url)
            except:
                pass

            products.append(product)

    return render_template("index.html", products=products, dates=history_dates, prices=history_prices)

@app.route("/price-history")
def price_history():
    try:
        url = request.args.get('url')
        days = request.args.get('days', type=int)
        
        if not url:
            return jsonify({"error": "URL parameter is required"}), 400
        
        dates, prices = get_price_history(url, days)
        
        if not dates or not prices:
            return jsonify({"error": "No historical data found"}), 404
            
        return jsonify({
            "status": "success",
            "dates": dates,
            "prices": prices
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    
def scheduled_tracking():
    urls = [
        # Add URLs to track daily
        "https://www.amazon.in/dp/EXAMPLE",
        "https://www.flipkart.com/item/p/EXAMPLE"
    ]
    for url in urls:
        if "amazon" in url:
            product = get_amazon_data(url)
        elif "flipkart" in url:
            product = get_flipkart_data(url)
        else:
            continue

        try:
            clean_price = int("".join(filter(str.isdigit, product["price"])))
            save_price(url, product["title"], clean_price, product["source"])
        except:
            pass

scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_tracking, 'interval', hours=24)
scheduler.start()

if __name__ == "__main__":
    app.run(debug=True)
