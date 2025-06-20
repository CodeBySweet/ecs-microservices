from flask import Flask, jsonify, render_template_string
import requests

app = Flask(__name__)

users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
]

@app.route('/')
@app.route('/user')
def home():
    try:
        auth_data = requests.get("http://auth.my-namespace.local/login", timeout=3).json()
    except Exception as e:
        auth_data = {"error": str(e)}

    try:
        product_data = requests.get("http://product.my-namespace.local/product/products", timeout=3).json()
    except Exception as e:
        product_data = [{"error": str(e)}]

    TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>User Service</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 2em; background: #f5f5f5; font-size: 1.2rem; }
            h1 { color: #2a2a2a; }
            table, th, td { border: 1px solid #aaa; border-collapse: collapse; padding: 8px; }
            h2 { margin-top: 2em; }
        </style>
    </head>
    <body>
        <h1>User Service</h1>

        <h2>Users List</h2>
        <table>
            <tr><th>ID</th><th>Name</th></tr>
            {% for u in users %}
                <tr><td>{{ u.id }}</td><td>{{ u.name }}</td></tr>
            {% endfor %}
        </table>

        <h2>Fetched Token from Auth Service</h2>
        <table>
            <tr><th>Token</th></tr>
            <tr><td>{{ auth_data.get('token', auth_data.get('error', 'N/A')) }}</td></tr>
        </table>

        <h2>Fetched Product Data from Product Service</h2>
        <table>
            <tr><th>ID</th><th>Name</th></tr>
            {% for p in product_data %}
                <tr><td>{{ p.get('id', '-') }}</td><td>{{ p.get('name', p.get('error', '-')) }}</td></tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """

    return render_template_string(TEMPLATE, users=users, auth_data=auth_data, product_data=product_data)

@app.route('/user/products')
def get_products():
    return jsonify(users)

@app.route('/user/health')
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3002)
