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

def get_price_history(url, days=None):
    with sqlite3.connect("prices.db") as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        query = """
            SELECT 
                strftime('%Y-%m-%d', timestamp) as date,
                price 
            FROM price_history 
            WHERE url=?
        """
        
        params = [url]
        
        if days:
            query += " AND date(timestamp) >= date('now', ?)"
            params.append(f'-{days} days')
        
        query += " ORDER BY timestamp ASC"
        
        c.execute(query, params)
        data = c.fetchall()
        
    dates = [row['date'] for row in data]
    prices = [row['price'] for row in data]
    
    return dates, prices
