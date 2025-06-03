# Comparely

## Overview

Comparely is a web application designed to help users compare prices of products from two major online retailers: Amazon and Flipkart.  It allows you to:

* **Compare Product Prices:** Enter the URLs of the same product from Amazon and Flipkart to see a side-by-side price comparison.
* **Search by Category:** Enter a category (e.g., "electronics", "clothing") to see a list of products from both Amazon and Flipkart, along with their prices.
* **View Wishlist:** Add products to your wishlist and view them later.

## Features

* **Product Comparison:** Compare prices, availability, and other details of a product from Amazon and Flipkart.
* **Category Search:** Search for products across Amazon and Flipkart within a specific category.
* **Wishlist:** Save products to your wishlist for later viewing.
* **User-Friendly Interface:** Clean and intuitive web interface.

## Technologies Used

* Python: Backend logic and web scraping.
* Flask: Web framework.
* Beautiful Soup: HTML parsing for web scraping.
* Requests: HTTP library for making requests.
* HTML/CSS: Frontend structure and styling
* Bootstrap: CSS framework.

## Setup

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
    cd your-repository-name
    ```

2.  **Set up a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set the Flask application:**

    ```bash
    export FLASK_APP=app.py
    ```

5.  **Run the application:**

    ```bash
    flask run --debug #Runs in debug mode
    ```

6.  **Open your browser:**

    * Visit `http://127.0.0.1:5000` to access the Price Tracker.

## Code Structure

* `app.py`: Main Flask application. Defines routes and integrates the scraping logic.
* `amazon_scraper.py`: Functions to scrape product data from Amazon.
* `flipkart_scraper.py`: Functions to scrape product data from Flipkart.
* `category_page_amazon.py`: Functions to scrape category listing from Amazon.
* `category_page_flipkart.py`: Functions to scrape category listing from Flipkart.
* `wishlist.py`: Functions to manage the user's wishlist.
* `index.html`: Main page for product comparison and category search.
* `wishlist.html`: Page to display the user's wishlist.
* `README.md`: Project documentation.

## Important Notes

* **Web Scraping:** Web scraping can be fragile. Websites change their structure, which may break the scrapers. The code may need to be updated periodically.
* **Error Handling:** The application includes error handling for network issues, HTTP errors, and parsing problems. Check the console output for error messages.
* **Logging:** The application uses the `logging` module to log important events and errors.
* **Database:** The wishlist functionality uses a SQLite database (`instance/pricetracker.db`). Ensure that the Flask instance folder is writable.
* **Security:** The application uses a secret key for Flask sessions. Ensure you change `app.secret_key = "your_secret_key"` to a strong, random key in `app.py`.
* **Reliability:** Always check the `robots.txt` file of any website before scraping it and ensure your scraper respects those rules. Scraping without permission may violate the website's terms of service.

## Contributions

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1.  Fork the repository.
2.  Create a new branch with a descriptive name (e.g., `feature/new-feature` or `bugfix/bug-name`).
3.  Make your changes.
4.  Write tests for your changes.
5.  Ensure that all tests pass.
6.  Submit a pull request.

### Contribution Guidelines

* Follow the existing code style.
* Write clear and concise commit messages.
* Provide a detailed description of your changes in the pull request.
* If you're adding a new feature, please include documentation.

### Areas for Contribution

* Add support for more e-commerce websites.
* Improve the accuracy and robustness of the web scraping.
* Enhance the user interface.
* Implement more advanced features, such as price tracking and alerts.
* Write more tests.
* Improve the application's performance.
