from flask import Flask, jsonify, render_template_string
import requests

app = Flask(__name__)

products = [
    {"id": 1, "name": "Laptop"},
    {"id": 2, "name": "Smartphone"},
    {"id": 3, "name": "Headphones"}
]

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Product Service</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 2em; background: #f5f5f5; font-size: 1.2rem; }
        h1 { color: #2a2a2a; }
        button { padding: 12px 24px; margin: 8px; font-size: 1rem; cursor: pointer; }
        table, th, td { border: 1px solid #aaa; border-collapse: collapse; padding: 8px; }
    </style>
</head>
<body>
    <h1>Product Service</h1>
    <table>
        <tr><th>ID</th><th>Name</th></tr>
        {% for p in products %}<tr><td>{{ p.id }}</td><td>{{ p.name }}</td></tr>{% endfor %}
    </table>
    <br>
    <button onclick="window.location.href='http://auth.my-namespace.local:3003/auth'">Go to Auth</button>
    <button onclick="window.location.href='http://user.my-namespace.local:3002/user'">Go to User</button>
</body>
</html>
"""

@app.route('/')
@app.route('/product')
def home():
    return render_template_string(TEMPLATE, products=products)

@app.route('/product/products')
def get_products():
    return jsonify(products)

@app.route('/product/health')
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3001)