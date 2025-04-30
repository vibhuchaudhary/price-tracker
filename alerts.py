from flask import Flask, session, url_for, redirect, flash
from db_utils import get_db  # Assuming db_utils.py is in the same directory
import sqlite3

def set_alert(app, product_id, desired_price):
    """Sets a price alert for a given product and user."""

    if not session.get('user_id'):
        return redirect(url_for('login'))  # Redirect to login if not logged in

    try:
        db = get_db(app)
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO PriceAlerts (user_id, product_id, desired_price) VALUES (?, ?, ?)",
            (session['user_id'], product_id, desired_price)
        )
        db.commit()
        flash('Price alert set!', 'success')
    except sqlite3.IntegrityError:
        flash('You already have an alert for this product.', 'warning')
    return redirect(url_for('product_detail', product_id=product_id))  # Adjust as needed

def check_price_alerts(app, get_current_amazon_price, get_current_flipkart_price, send_price_drop_alert):
    """
    Checks for price drops and sends alerts. This function needs to be adapted
    to your specific notification system (e.g., email).
    """

    db = get_db(app)
    cursor = db.cursor()
    cursor.execute(
        "SELECT a.alert_id, a.user_id, a.product_id, a.desired_price, p.name, p.amazon_url, p.flipkart_url "
        "FROM PriceAlerts a JOIN Products p ON a.product_id = p.product_id"
    )
    alerts = cursor.fetchall()

    for alert in alerts:
        amazon_price = get_current_amazon_price(alert['amazon_url'])  # Implement these functions
        flipkart_price = get_current_flipkart_price(alert['flipkart_url'])  # Implement these functions
        current_price = min(price for price in [amazon_price, flipkart_price] if price is not None)

        if current_price is not None and current_price <= alert['desired_price']:
            send_price_drop_alert(app, alert['user_id'], alert['name'], current_price, alert['amazon_url'], alert['flipkart_url'])
            cursor.execute("DELETE FROM PriceAlerts WHERE alert_id = ?", (alert['alert_id'],))
            db.commit()

def send_price_drop_alert(app, user_id, product_name, current_price, amazon_url, flipkart_url):
    """
    Placeholder for sending the actual notification.  You'll need to implement
    email sending or another notification mechanism here.
    """
    print(f"Price alert! User: {user_id}, Product: {product_name}, Current Price: {current_price}, Amazon: {amazon_url}, Flipkart: {flipkart_url}")
    pass  # Replace with actual notification logic