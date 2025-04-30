from flask import Flask, render_template, request, url_for, redirect, flash
import logging

from scrapers.amazon_scraper import scrape_amazon_product
from scrapers.flipkart_scraper import scrape_flipkart_product
from scrapers.category_page_flipkart import scrape_flipkart_category
from scrapers.category_page_amazon import scrape_amazon_category

# Initialize Flask application
app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a strong random key

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Dummy wishlist (replace with a database in a real app)
wishlist = []


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Handles the main route of the application, allowing users to compare products
    and search for categories.
    """
    amazon_data = None
    flipkart_data = None
    category_results_flipkart = None
    category_results_amazon = None
    lowest_price_product = None

    if request.method == "POST":
        amazon_url = request.form.get("amazon_url", "").strip()
        flipkart_url = request.form.get("flipkart_url", "").strip()
        category_name = request.form.get("category_name", "").strip()
        num_results_str = request.form.get("num_results", "5")  # Get as string first
        find_lowest = request.form.get("find_lowest", "no").lower()

        # Product Comparison Logic
        if amazon_url and flipkart_url:
            try:
                amazon_data = scrape_amazon_product(amazon_url)
                flipkart_data = scrape_flipkart_product(flipkart_url)
            except Exception as e:
                logging.error(f"Error during product comparison: {e}")
                flash("Failed to compare products. Please check the URLs.", "danger")

        # Category Search Logic
        elif category_name:
            try:
                num_results = int(num_results_str)  # Convert to integer
            except ValueError:
                num_results = 5
                flash("Invalid number of results. Using default (5).", "warning")
            except Exception as e:
                logging.error(f"Error processing number of results: {e}")
                num_results = 5
                flash("An error occurred while processing your request.", "danger")

            try:
                # Scrape Flipkart Category
                flipkart_category_results = scrape_flipkart_category(category_name)
                if flipkart_category_results:
                    category_results_flipkart = flipkart_category_results[:num_results]

                    # Find lowest price product in Flipkart results
                    if find_lowest == "yes":
                        valid_flipkart_products = [p for p in flipkart_category_results if p.get("price") is not None]
                        if valid_flipkart_products:
                            lowest_price_flipkart = min(valid_flipkart_products, key=lambda x: x['price'])
                            lowest_price_product = [lowest_price_flipkart]
                        else:
                            lowest_price_product = []  # Initialize to empty list
                else:
                    flash("Could not retrieve products from Flipkart.", "warning")

                # Scrape Amazon Category
                amazon_category_results, amazon_lowest = scrape_amazon_category(category_name)
                if amazon_category_results:
                    category_results_amazon = amazon_category_results[:num_results]

                    # Compare and update lowest price product
                    if find_lowest == "yes" and amazon_lowest:
                        if lowest_price_product:
                            if amazon_lowest['price_value'] < lowest_price_product[0]['price_value']:
                                lowest_price_product = [amazon_lowest]
                        else:
                            lowest_price_product = [amazon_lowest]
                else:
                    flash("Could not retrieve products from Amazon.", "warning")

            except Exception as e:
                logging.error(f"Error during category search: {e}")
                flash("An error occurred while searching for products.", "danger")

    return render_template(
        "index.html",
        amazon=amazon_data,
        flipkart=flipkart_data,
        category_results_flipkart=category_results_flipkart,
        category_results_amazon=category_results_amazon,
        lowest_price_product=lowest_price_product
    )


@app.route("/add_to_wishlist", methods=["POST"])
def add_to_wishlist_route():
    """
    Handles adding a product to the user's wishlist.
    """
    title = request.form.get("title")
    price = request.form.get("price")
    link = request.form.get("link")
    if title and price and link:
        wishlist.append({"title": title, "price": price, "link": link})
        flash(f"Added {title} to wishlist!", "success")
        logging.info(f"Added '{title}' to wishlist.")
    else:
        flash("Could not add to wishlist. Missing product details.", "danger")
        logging.warning("Attempted to add to wishlist with missing details.")
    return redirect(url_for("index"))


@app.route("/remove_from_wishlist", methods=["POST"])
def remove_from_wishlist():
    """
    Handles removing a product from the user's wishlist.
    """
    title = request.form.get("title")
    if title:
        for item in wishlist:
            if item["title"] == title:
                wishlist.remove(item)
                flash(f"Removed {title} from wishlist!", "info")
                logging.info(f"Removed '{title}' from wishlist.")
                return redirect(url_for("view_wishlist"))  # Redirect and exit
        flash(f"{title} not found in wishlist.", "warning")
        logging.warning(f"'{title}' not found in wishlist.")
    else:
        flash("Could not remove from wishlist. Missing product title.", "danger")
        logging.warning("Attempted to remove from wishlist without title.")
    return redirect(url_for("view_wishlist"))


@app.route("/wishlist")
def view_wishlist():
    """
    Displays the user's wishlist.
    """
    return render_template("wishlist.html", wishlist=wishlist)


if __name__ == "__main__":
    app.run(debug=True)