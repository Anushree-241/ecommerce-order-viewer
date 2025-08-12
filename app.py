from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
DATABASE = "ecom.db"

def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv

# @app.route("/")
# def home():
#     return render_template("index.html")

@app.route("/search", methods=["GET", "POST"])
def search_users():
    results = []
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        email = request.form.get("email", "").strip()

        query = "SELECT * FROM users WHERE 1=1"
        params = []
        if first_name:
            query += " AND first_name LIKE ?"
            params.append(f"%{first_name}%")
        if email:
            query += " AND email LIKE ?"
            params.append(f"%{email}%")

        results = query_db(query, params)
    
    return render_template("search.html", results=results)

@app.route("/user/<int:user_id>/orders")
def view_orders(user_id):
    orders = query_db("SELECT * FROM orders WHERE user_id = ?", (user_id,))
    return render_template("orders.html", orders=orders, user_id=user_id)

@app.route("/order/<int:order_id>/items")
def view_order_items(order_id):
    items = query_db("""
        SELECT order_items.*, products.name, products.brand, products.retail_price
        FROM order_items
        JOIN products ON order_items.product_id = products.id
        WHERE order_items.order_id = ?
    """, (order_id,))
    return render_template("order_items.html", items=items, order_id=order_id)

if __name__ == "__main__":
    app.run(debug=True)
