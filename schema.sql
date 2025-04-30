DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS PriceHistory;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Wishlist;
DROP TABLE IF EXISTS PriceAlerts;
DROP TABLE IF EXISTS Ratings;

CREATE TABLE Products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amazon_url TEXT,
    flipkart_url TEXT,
    name TEXT,
    category TEXT,
    image_url TEXT
);

CREATE TABLE PriceHistory (
    price_history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    price REAL NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    retailer TEXT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL  -- Store hashed passwords!
);

CREATE TABLE Wishlist (
    wishlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    product_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id),
    UNIQUE (user_id, product_id)
);

CREATE TABLE PriceAlerts (
    alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    product_id INTEGER,
    desired_price REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

CREATE TABLE Ratings (
    rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    rating_value REAL NOT NULL,
    rating_count INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);