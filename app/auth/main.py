from flask import Flask, jsonify, render_template_string
import requests

app = Flask(__name__)

TOKENS = [
    {"user": "alice@example.com", "token": "abc123xyz"},
    {"user": "bob@example.com", "token": "def456uvw"}
]

@app.route('/auth')
def auth_root():
    TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Auth Service</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 2em; background: #f0f4f8; font-size: 1.2rem; color: #333; }
            h1 { color: #007acc; }
            table, th, td { border: 1px solid #ddd; border-collapse: collapse; padding: 8px; }
            table { background: #fff; box-shadow: 0 0 10px rgba(0,0,0,0.05); }
            th { background-color: #f7f7f7; }
            .nav-buttons { margin-top: 2em; }
            .btn { padding: 10px 16px; margin: 5px; border: none; background: #007acc; color: white; border-radius: 5px; text-decoration: none; font-weight: bold; }
            .btn:hover { background: #005f99; }
        </style>
    </head>
    <body>
        <h1>🔐 Auth Service</h1>
        <p><strong>Status:</strong> Auth Service is running independently.</p>

        <h2>Tokens</h2>
        <table>
            <tr><th>User</th><th>Token</th></tr>
            {% for t in tokens %}
                <tr><td>{{ t.user }}</td><td>{{ t.token }}</td></tr>
            {% endfor %}
        </table>

        <div class="nav-buttons">
            <a href="/get-user" class="btn">🔄 Fetch User Info</a>
            <a href="/get-product" class="btn">🛍 Fetch Product Info</a>
        </div>
    </body>
    </html>
    """
    return render_template_string(TEMPLATE, tokens=TOKENS)

@app.route('/get-user')
def get_user():
    try:
        response = requests.get("http://user.my-namespace.local:3002/user", timeout=3)
        user_data = response.json()
        return jsonify({"message": "Fetched from User Service", "data": user_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-product')
def get_product():
    try:
        response = requests.get("http://product.my-namespace.local:3001/product", timeout=3)
        product_data = response.json()
        return jsonify({"message": "Fetched from Product Service", "data": product_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/auth/health')
def health():
    return "ok", 200

@app.route('/login')
def login():
    return jsonify({"token": "dummy-jwt-token"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3003)
