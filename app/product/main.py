from flask import Flask, jsonify, render_template_string, request
import requests

app = Flask(__name__)

products = [
    {"id": 1, "name": "Laptop"},
    {"id": 2, "name": "Smartphone"},
    {"id": 3, "name": "Headphones"}
]

@app.route('/product')
def home():
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
            .nav-buttons { margin-top: 2em; }
            .btn { padding: 10px 16px; margin: 5px; border: none; background: #007acc; color: white; border-radius: 5px; text-decoration: none; font-weight: bold; }
            .btn:hover { background: #005f99; }
        </style>
    </head>
    <body>
        <h1>🛍️ Product Service</h1>
        <p><strong>Status:</strong> Product service is running independently.</p>

        <div class="nav-buttons">
            <a href="/fetch-with-auth" class="btn">🔐 Get Products with Token Validation</a>
        </div>
    </body>
    </html>
    """
    return render_template_string(TEMPLATE)

@app.route('/fetch-with-auth')
def fetch_with_auth():
    try:
        # Simulate token validation by calling auth
        auth_resp = requests.get("http://auth.my-namespace.local:3003/login", timeout=3)
        token = auth_resp.json().get("token")

        # Call user service to simulate user context
        user_resp = requests.get("http://user.my-namespace.local:3002/user", timeout=3)
        users = user_resp.json()

        return jsonify({
            "validated_token": token,
            "products": products,
            "user_context": users
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/product/health')
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3001)
