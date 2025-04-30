from flask import Flask, render_template, request
from amazon_scraper import scrape_amazon_product
from flipkart_scraper import scrape_flipkart_product
from category_page_flipkart import scrape_flipkart_category
from category_page_amazon import scrape_amazon_organic_listings_extended_lowest

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    amazon_data = flipkart_data = category_results_flipkart = category_results_amazon = None
    lowest_price_product = None

    if request.method == "POST":
        amazon_url = request.form.get("amazon_url", "").strip()
        flipkart_url = request.form.get("flipkart_url", "").strip()
        category_name = request.form.get("category_name", "").strip()
        num_results = request.form.get("num_results", "5")
        find_lowest = request.form.get("find_lowest", "no")

        if amazon_url and flipkart_url:
            amazon_data = scrape_amazon_product(amazon_url)
            flipkart_data = scrape_flipkart_product(flipkart_url)

        elif category_name:
            try:
                num_results = int(num_results)
            except ValueError:
                num_results = 5

            # Scrape Flipkart Category
            flipkart_category_results = scrape_flipkart_category(category_name)  # Changed this line
            if flipkart_category_results:
                category_results_flipkart = flipkart_category_results[:num_results]
                if find_lowest.lower() == "yes":
                    valid_flipkart_products = [p for p in flipkart_category_results if p.get("price") is not None]
                    if valid_flipkart_products:
                        lowest_price_flipkart = min(valid_flipkart_products, key=lambda x: x['price'])
                        lowest_price_product = [lowest_price_flipkart]
                    else:
                        lowest_price_product = []  # Initialize to empty list

            # Scrape Amazon Category
            amazon_category_results, amazon_lowest = scrape_amazon_organic_listings_extended_lowest(category_name)
            if amazon_category_results:
                category_results_amazon = amazon_category_results[:num_results]
                if find_lowest.lower() == "yes" and amazon_lowest:
                    if lowest_price_product:
                        if amazon_lowest.get('price_value') is not None and lowest_price_product[0].get('price') is not None and amazon_lowest['price_value'] < lowest_price_product[0]['price']:
                            lowest_price_product = [amazon_lowest]
                    else:
                        lowest_price_product = [amazon_lowest]

    return render_template(
        "index.html",
        amazon=amazon_data,
        flipkart=flipkart_data,
        category_results_flipkart=category_results_flipkart,
        category_results_amazon=category_results_amazon,
        lowest_price_product=lowest_price_product
    )

if __name__ == "__main__":
    app.run(debug=True)