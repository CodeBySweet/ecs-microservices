from flask import Flask, jsonify, render_template_string
import requests

app = Flask(__name__)

products = [
    {"id": 1, "name": "Laptop"},
    {"id": 2, "name": "Smartphone"},
    {"id": 3, "name": "Headphones"}
]

@app.route('/')
@app.route('/product')
def home():
    try:
        auth_data = requests.get("http://auth.my-namespace.local/login", timeout=3).json()
    except Exception as e:
        auth_data = {"error": str(e)}

    try:
        user_data = requests.get("http://user.my-namespace.local/user/products", timeout=3).json()
    except Exception as e:
        user_data = [{"error": str(e)}]

    TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Product Service</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 2em; background: #f5f5f5; font-size: 1.2rem; }
            h1 { color: #2a2a2a; }
            table, th, td { border: 1px solid #aaa; border-collapse: collapse; padding: 8px; }
            h2 { margin-top: 2em; }
        </style>
    </head>
    <body>
        <h1>Product Service</h1>

        <h2>Product List</h2>
        <table>
            <tr><th>ID</th><th>Name</th></tr>
            {% for p in products %}
                <tr><td>{{ p.id }}</td><td>{{ p.name }}</td></tr>
            {% endfor %}
        </table>

        <h2>Fetched Token from Auth Service</h2>
        <table>
            <tr><th>Token</th></tr>
            <tr><td>{{ auth_data.get('token', auth_data.get('error', 'N/A')) }}</td></tr>
        </table>

        <h2>Fetched User Data from User Service</h2>
        <table>
            <tr><th>ID</th><th>Name</th></tr>
            {% for u in user_data %}
                <tr><td>{{ u.get('id', '-') }}</td><td>{{ u.get('name', u.get('error', '-')) }}</td></tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """

    return render_template_string(TEMPLATE, products=products, auth_data=auth_data, user_data=user_data)

@app.route('/product/products')
def get_products():
    return jsonify(products)

@app.route('/product/health')
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3001)
