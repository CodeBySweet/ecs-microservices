from flask import Flask, jsonify, render_template_string
import requests

app = Flask(__name__)

TOKENS = [
    {"user": "alice@example.com", "token": "abc123xyz"},
    {"user": "bob@example.com", "token": "def456uvw"}
]

@app.route('/')
@app.route('/auth')
def auth_root():
    # Get external data
    try:
        product_data = requests.get("http://product.my-namespace.local:3001/product/products", timeout=3).json()
    except Exception as e:
        product_data = [{"error": str(e)}]

    try:
        user_data = requests.get("http://user.my-namespace.local:3002/user/products", timeout=3).json()
    except Exception as e:
        user_data = [{"error": str(e)}]

    TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Auth Service</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 2em; background: #f9f9f9; font-size: 1.2rem; }
            h1 { color: #333; }
            table, th, td { border: 1px solid #aaa; border-collapse: collapse; padding: 8px; }
            h2 { margin-top: 2em; }
        </style>
    </head>
    <body>
        <h1>Auth Service</h1>
        <p><strong>Status:</strong> Auth Service running!</p>

        <h2>Tokens</h2>
        <table>
            <tr><th>User</th><th>Token</th></tr>
            {% for t in tokens %}<tr><td>{{ t.user }}</td><td>{{ t.token }}</td></tr>{% endfor %}
        </table>

        <h2>Fetched Product Data from Product Service</h2>
        <table>
            <tr><th>ID</th><th>Name</th></tr>
            {% for p in product_data %}
                <tr><td>{{ p.get('id', '-') }}</td><td>{{ p.get('name', p.get('error', '-')) }}</td></tr>
            {% endfor %}
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

    return render_template_string(TEMPLATE, tokens=TOKENS, product_data=product_data, user_data=user_data)

@app.route('/auth/health')
def health():
    return "ok", 200

@app.route('/login')
def login():
    return jsonify({"token": "dummy-jwt-token"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3003)
