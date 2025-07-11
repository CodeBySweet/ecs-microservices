from flask import Flask, jsonify, render_template_string
import requests

app = Flask(__name__)

products = [
    {"id": 1, "name": "Laptop"},
    {"id": 2, "name": "Smartphone"},
    {"id": 3, "name": "Headphones"}
]

@app.route('/product')
def home():
    try:
        auth_resp = requests.get("http://auth.my-namespace.local:3003/login", timeout=3)
        token = auth_resp.json().get("token")
        auth_status = "Success"
    except Exception as e:
        token = {"error": str(e)}
        auth_status = "Failed"

    try:
        user_resp = requests.get("http://user.my-namespace.local:3002/user/data", timeout=3)
        user_data = user_resp.json()
        user_status = "Success"
    except Exception as e:
        user_data = {"error": str(e)}
        user_status = "Failed"

    TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Product Service</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 2em; background: #f0f4f8; font-size: 1.2rem; color: #333; }
            h1 { color: #007acc; }
            table, th, td { border: 1px solid #ddd; border-collapse: collapse; padding: 8px; }
            table { background: #fff; box-shadow: 0 0 10px rgba(0,0,0,0.05); }
            th { background-color: #f7f7f7; }
            pre { background: #eef; padding: 10px; border-radius: 5px; overflow-x: auto; }
        </style>
    </head>
    <body>
        <h1>🛍 Product Service</h1>
        <p><strong>Status:</strong> Running and calling other services...</p>

        <h2>📦 Product List</h2>
        <table>
            <tr><th>ID</th><th>Name</th></tr>
            {% for p in products %}
                <tr><td>{{ p.id }}</td><td>{{ p.name }}</td></tr>
            {% endfor %}
        </table>

        <h2>👤 Called User Service - {{ user_status }}</h2>
        <pre>{{ user_data | tojson(indent=2) }}</pre>
    </body>
    </html>
    """
    return render_template_string(
        TEMPLATE,
        products=products,
        token=token,
        user_data=user_data,
        auth_status=auth_status,
        user_status=user_status
    )

@app.route('/product/products')
def get_products():
    return jsonify(products)

@app.route('/product/health')
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3001)
