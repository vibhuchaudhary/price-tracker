import sqlite3
from flask import Flask, g

def get_db(app):
    """Connect to the application's configured SQLite database. The
    connection is unique for each request and will be reused if the
    same function is called again.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row  # Return rows as dictionaries
    return g.db

def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(app):
    """Initializes the database by executing the schema.sql script."""

    with app.app_context():
        db = get_db(app)
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def query_db(app, query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    cur = get_db(app).execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv