import sqlite3

def init_db():
    with sqlite3.connect("prices.db") as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS price_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        url TEXT,
                        title TEXT,
                        price INTEGER,
                        source TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )''')

def save_price(url, title, price, source):
    with sqlite3.connect("prices.db") as conn:
        c = conn.cursor()
        c.execute("INSERT INTO price_history (url, title, price, source) VALUES (?, ?, ?, ?)",
                  (url, title, price, source))

def get_price_history(url):
    with sqlite3.connect("prices.db") as conn:
        c = conn.cursor()
        c.execute("SELECT timestamp, price FROM price_history WHERE url=? ORDER BY timestamp ASC", (url,))
        data = c.fetchall()
    dates = [row[0] for row in data]
    prices = [row[1] for row in data]
    return dates, prices
