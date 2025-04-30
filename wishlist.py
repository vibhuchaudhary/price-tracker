# wishlist.py
from flask import Flask, session, url_for, redirect, request, flash
from db_utils import get_db
import sqlite3

def add_to_wishlist(app, product_id):
    """Adds a product to the user's wishlist."""

    if not session.get('user_id'):
        flash('You must be logged in to add to wishlist.', 'danger')
        return redirect(url_for('login'))

    try:
        db = get_db(app)
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO Wishlist (user_id, product_id) VALUES (?, ?)",
            (session['user_id'], product_id)
        )
        db.commit()
        flash('Added to wishlist!', 'success')  # Flash success message
    except sqlite3.IntegrityError:
        flash('Product already in wishlist.', 'info')  # Flash info message if already exists
    except sqlite3.Error as e:
        flash(f'Database error: {e}', 'danger') # General database error
    return redirect(request.referrer or url_for('index')) # Redirect back or to index

def remove_from_wishlist(app, product_id):
    """Removes a product from the user's wishlist."""

    if not session.get('user_id'):
        flash('You must be logged in to remove from wishlist.', 'danger')
        return redirect(url_for('login'))

    db = get_db(app)
    cursor = db.cursor()
    cursor.execute(
        "DELETE FROM Wishlist WHERE user_id = ? AND product_id = ?",
        (session['user_id'], product_id)
    )
    db.commit()
    flash('Removed from wishlist!', 'success')
    return redirect(url_for('wishlist'))

def get_wishlist(app, user_id):
    """Retrieves the user's wishlist products."""

    db = get_db(app)
    cursor = db.cursor()
    cursor.execute(
        "SELECT p.* FROM Products p JOIN Wishlist w ON p.product_id = w.product_id WHERE w.user_id = ?",
        (user_id,)
    )
    return cursor.fetchall()