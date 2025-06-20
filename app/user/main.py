from flask import Flask, jsonify, render_template_string
import requests

app = Flask(__name__)

users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
]

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>User Service</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 2em; background: #f5f5f5; font-size: 1.2rem; }
        h1 { color: #2a2a2a; }
        button { padding: 12px 24px; margin: 8px; font-size: 1rem; cursor: pointer; }
        table, th, td { border: 1px solid #aaa; border-collapse: collapse; padding: 8px; }
    </style>
</head>
<body>
    <h1>User Service</h1>
    <table>
        <tr><th>ID</th><th>Name</th></tr>
        {% for u in users %}<tr><td>{{ u.id }}</td><td>{{ u.name }}</td></tr>{% endfor %}
    </table>
    <br>
    <button onclick="window.location.href='http://auth.my-namespace.local/auth'">Go to Auth</button>
    <button onclick="window.location.href='http://product.my-namespace.local/product'">Go to Product</button>
</body>
</html>
"""

@app.route('/')
@app.route('/user')
def home():
    return render_template_string(TEMPLATE, users=users)

@app.route('/user/products')
def get_products():
    return jsonify(users)

@app.route('/user/health')
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3002)
