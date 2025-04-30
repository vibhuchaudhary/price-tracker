from flask import Flask, render_template, request
from amazon_scraper import scrape_amazon_product
from flipkart_scraper import scrape_flipkart_product
from category_page_flipkart import scrape_flipkart_category  # <-- NEW: for Flipkart category scraping

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    amazon_data = flipkart_data = category_results = None
    lowest_price_product = None

    if request.method == "POST":
        amazon_url = request.form.get("amazon_url", "").strip()
        flipkart_url = request.form.get("flipkart_url", "").strip()
        category_name = request.form.get("category_name", "").strip()
        num_results = request.form.get("num_results", 5)
        find_lowest = request.form.get("find_lowest", "no")

        if amazon_url and flipkart_url:
            amazon_data = scrape_amazon_product(amazon_url)
            flipkart_data = scrape_flipkart_product(flipkart_url)

        elif category_name:
            try:
                num_results = int(num_results)
            except ValueError:
                num_results = 5

            all_results = scrape_flipkart_category(category_name)
            if all_results:
                category_results = all_results[:num_results]

                if find_lowest.lower() == "yes":
                    # Find product with minimum price
                    valid_products = [prod for prod in all_results if prod.get("price") is not None]
                    if valid_products:
                        lowest_price_product = min(valid_products, key=lambda x: x["price"])

    return render_template(
        "index.html",
        amazon=amazon_data,
        flipkart=flipkart_data,
        category_results=category_results,
        lowest_price_product=lowest_price_product
    )

if __name__ == "__main__":
    app.run(debug=True)
