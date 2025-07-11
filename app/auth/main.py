from flask import Flask, jsonify, render_template_string
import requests

app = Flask(__name__)

TOKENS = [
    {"user": "alice@example.com", "token": "abc123xyz"},
    {"user": "bob@example.com", "token": "def456uvw"}
]

@app.route('/auth')
def auth_root():
    # Simulate API calls to user and product services
    try:
        user_response = requests.get("http://user.my-namespace.local:3002/user", timeout=3)
        user_data = user_response.json()
        user_status = "Success"
    except Exception as e:
        user_data = {"error": str(e)}
        user_status = "Failed"

    try:
        product_response = requests.get("http://product.my-namespace.local:3001/product", timeout=3)
        product_data = product_response.json()
        product_status = "Success"
    except Exception as e:
        product_data = {"error": str(e)}
        product_status = "Failed"

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
            pre { background: #eef; padding: 10px; border-radius: 5px; overflow-x: auto; }
        </style>
    </head>
    <body>
        <h1>🔐 Auth Service</h1>
        <p><strong>Status:</strong> Running and calling other services...</p>

        <h2>Tokens</h2>
        <table>
            <tr><th>User</th><th>Token</th></tr>
            {% for t in tokens %}
                <tr><td>{{ t.user }}</td><td>{{ t.token }}</td></tr>
            {% endfor %}
        </table>

        <h2>📡 Called User Service - {{ user_status }}</h2>
        <pre>{{ user_data | tojson(indent=2) }}</pre>

        <h2>📡 Called Product Service - {{ product_status }}</h2>
        <pre>{{ product_data | tojson(indent=2) }}</pre>
    </body>
    </html>
    """
    return render_template_string(
        TEMPLATE,
        tokens=TOKENS,
        user_data=user_data,
        product_data=product_data,
        user_status=user_status,
        product_status=product_status
    )

@app.route('/auth/health')
def health():
    return "ok", 200

@app.route('/login')
def login():
    return jsonify({"token": "dummy-jwt-token"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3003)
