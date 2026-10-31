from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
DB_PATH = Path(__file__).parent / "bookstore.db"

SEED_BOOKS = [
    ("The Alchemist", "Paulo Coelho", 299.00, "A journey about following your dreams."),
    ("Wings of Fire", "A. P. J. Abdul Kalam", 250.00, "The inspiring autobiography of Dr. Kalam."),
    ("Atomic Habits", "James Clear", 399.00, "Small habits that create remarkable results."),
    ("Python Crash Course", "Eric Matthes", 550.00, "A hands-on introduction to Python.")
]

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect_db() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT NOT NULL
        )""")
        count = conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
        if count == 0:
            conn.executemany(
                "INSERT INTO books (title, author, price, description) VALUES (?, ?, ?, ?)",
                SEED_BOOKS
            )

@app.route("/")
def home():
    with connect_db() as conn:
        books = conn.execute("SELECT * FROM books ORDER BY id DESC").fetchall()
    return render_template("index.html", books=books)

@app.route("/add", methods=["POST"])
def add_book():
    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()
    description = request.form.get("description", "").strip()
    try:
        price = float(request.form.get("price", "0"))
        if price <= 0:
            raise ValueError
    except ValueError:
        flash("Enter a valid price greater than zero.")
        return redirect(url_for("home"))
    if not title or not author or not description:
        flash("Please fill in all book details.")
        return redirect(url_for("home"))
    with connect_db() as conn:
        conn.execute(
            "INSERT INTO books (title, author, price, description) VALUES (?, ?, ?, ?)",
            (title, author, price, description)
        )
    flash("Book added successfully!")
    return redirect(url_for("home"))

@app.route("/health")
def health():
    return {"status": "healthy"}, 200

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
