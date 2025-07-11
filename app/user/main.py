from flask import Flask, jsonify, render_template_string
import requests

app = Flask(__name__)

users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
]

@app.route('/user')
def home():
    try:
        auth_status = requests.get("http://auth.my-namespace.local:3003/auth/health", timeout=2).text
    except Exception as e:
        auth_status = f"Unavailable ({e})"

    try:
        product_status = requests.get("http://product.my-namespace.local:3001/product/health", timeout=2).text
    except Exception as e:
        product_status = f"Unavailable ({e})"

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
            .nav-buttons { margin-top: 2em; }
            .btn { padding: 10px 16px; margin: 5px; border: none; background: #007acc; color: white; border-radius: 5px; text-decoration: none; font-weight: bold; }
            .btn:hover { background: #005f99; }
            .status { font-size: 0.9rem; margin-left: 0.5em; color: green; }
            .error { color: red; }
        </style>
    </head>
    <body>
        <h1>👤 User Service</h1>
        <p><strong>Status:</strong> User service is running independently.</p>

        <h2>User List</h2>
        <table>
            <tr><th>ID</th><th>Name</th></tr>
            {% for u in users %}
                <tr><td>{{ u.id }}</td><td>{{ u.name }}</td></tr>
            {% endfor %}
        </table>

        <div class="nav-buttons">
            <a href="http://auth.my-namespace.local:3003/auth" class="btn">➡️ Go to Auth</a>
            <span class="status {% if 'ok' not in auth_status %}error{% endif %}">{{ auth_status }}</span>

            <a href="http://product.my-namespace.local:3001/product" class="btn">➡️ Go to Product</a>
            <span class="status {% if 'ok' not in product_status %}error{% endif %}">{{ product_status }}</span>
        </div>
    </body>
    </html>
    """
    return render_template_string(TEMPLATE, users=users, auth_status=auth_status, product_status=product_status)

@app.route('/user')
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
