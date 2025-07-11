from flask import Flask, jsonify, render_template_string, request
import requests

app = Flask(__name__)

users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
]

@app.route('/user')
def home():
    try:
        auth_resp = requests.get("http://auth.my-namespace.local:3003/login", timeout=3)
        token = auth_resp.json().get("token")
        auth_status = "Success"
    except Exception as e:
        token = {"error": str(e)}
        auth_status = "Failed"
    try:
        product_resp = requests.get("http://product.my-namespace.local:3001/product/products", timeout=3)
        product_data = product_resp.json()
        product_status = "Success"
    except Exception as e:
        product_data = {"error": str(e)}
        product_status = "Failed"

    TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>User Service</title>
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
        <h1>👤 User Service</h1>
        <p><strong>Status:</strong> Running and calling other services...</p>

        <h2>User List</h2>
        <table>
            <tr><th>ID</th><th>Name</th></tr>
            {% for u in users %}
                <tr><td>{{ u.id }}</td><td>{{ u.name }}</td></tr>
            {% endfor %}
        </table>

        <h2>🔐 Called Auth Service - {{ auth_status }}</h2>
        <pre>{{ token | tojson(indent=2) }}</pre>

        <h2>🛍 Called Product Service - {{ product_status }}</h2>
        <pre>{{ product_data | tojson(indent=2) }}</pre>
    </body>
    </html>
    """
    return render_template_string(
        TEMPLATE,
        users=users,
        token=token,
        product_data=product_data,
        auth_status=auth_status,
        product_status=product_status
    )

@app.route('/user/data')
def get_users():
    return jsonify(users)

@app.route('/user/preferences')
def get_preferences():
    preferences = {
        1: {"theme": "dark", "language": "en"},
        2: {"theme": "light", "language": "es"}
    }
    user_id = int(request.args.get("user_id", 1))
    return jsonify(preferences.get(user_id, {}))

@app.route('/user/health')
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3002)
