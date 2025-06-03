# wishlist.py
from flask import Flask, session, url_for, redirect, request, flash
from db_utils import get_db
import sqlite3
import logging

# Configure logging (consider a more robust setup for production)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def add_to_wishlist(app, product_id):
    """
    Adds a product to the user's wishlist.

    Args:
        app: The Flask application instance.
        product_id: The ID of the product to add.

    Returns:
        A Flask redirect response.
    """

    # Check if the user is logged in
    if not session.get('user_id'):
        flash('You must be logged in to add to wishlist.', 'danger')
        return redirect(url_for('login'))  # Assuming 'login' is your login route

    try:
        # Get database connection
        db = get_db(app)
        cursor = db.cursor()

        # Execute the INSERT query
        cursor.execute(
            "INSERT INTO Wishlist (user_id, product_id) VALUES (?, ?)",
            (session['user_id'], product_id)
        )
        db.commit()  # Save changes to the database
        flash('Added to wishlist!', 'success')  # Flash a success message

    except sqlite3.IntegrityError:
        # Handle the case where the product is already in the wishlist
        flash('Product already in wishlist.', 'info')
    except sqlite3.Error as e:
        # Handle general database errors
        logging.error(f"Database error while adding to wishlist: {e}")
        flash(f'Database error: {e}', 'danger')
    except Exception as e:
        # Catch any unexpected exceptions
        logging.error(f"Unexpected error while adding to wishlist: {e}")
        flash('An unexpected error occurred.', 'danger')
    finally:
        # Ensure the database connection is closed (best practice)
        if db:
            db.close()

    # Redirect the user back to the previous page or the index page
    return redirect(request.referrer or url_for('index'))


def remove_from_wishlist(app, product_id):
    """
    Removes a product from the user's wishlist.

    Args:
        app: The Flask application instance.
        product_id: The ID of the product to remove.

    Returns:
        A Flask redirect response.
    """

    # Check if the user is logged in
    if not session.get('user_id'):
        flash('You must be logged in to remove from wishlist.', 'danger')
        return redirect(url_for('login'))  # Redirect to login page

    try:
        # Get database connection
        db = get_db(app)
        cursor = db.cursor()

        # Execute the DELETE query
        cursor.execute(
            "DELETE FROM Wishlist WHERE user_id = ? AND product_id = ?",
            (session['user_id'], product_id)
        )
        db.commit()  # Save changes
        flash('Removed from wishlist!', 'info')

    except sqlite3.Error as e:
        # Handle database errors
        logging.error(f"Database error while removing from wishlist: {e}")
        flash(f'Database error: {e}', 'danger')
    except Exception as e:
        # Handle unexpected errors
        logging.error(f"Unexpected error while removing from wishlist: {e}")
        flash('An unexpected error occurred.', 'danger')
    finally:
        # Ensure the database connection is closed
        if db:
            db.close()

    return redirect(url_for('wishlist'))  # Redirect back to the wishlist page


def get_wishlist(app, user_id):
    """
    Retrieves the user's wishlist products.

    Args:
        app: The Flask application instance.
        user_id: The ID of the user whose wishlist is to be retrieved.

    Returns:
        A list of product dictionaries or None if there's an error.
    """

    try:
        # Get database connection
        db = get_db(app)
        cursor = db.cursor()

        # Execute the SELECT query to fetch products in the wishlist
        cursor.execute(
            """
            SELECT p.* FROM Products p
            JOIN Wishlist w ON p.id = w.product_id
            WHERE w.user_id = ?
            """,
            (user_id,)
        )

        products = [
            {
                'id': row[0],
                'name': row[1],
                'price': row[2],
                'description': row[3],
                'image_url': row[4]
            }
            for row in cursor.fetchall()
        ]

        return products

    except sqlite3.Error as e:
        # Handle database errors
        logging.error(f"Database error while getting wishlist: {e}")
        flash(f'Database error: {e}', 'danger')
        return None
    except Exception as e:
        # Handle unexpected errors
        logging.error(f"Unexpected error while getting wishlist: {e}")
        flash('An unexpected error occurred.', 'danger')
        return None
    finally:
        # Ensure the database connection is closed
        if db:
            db.close()