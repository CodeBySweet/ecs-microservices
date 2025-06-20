from flask import Flask, jsonify, render_template_string
import requests

app = Flask(__name__)

TOKENS = [
    {"user": "alice@example.com", "token": "abc123xyz"},
    {"user": "bob@example.com", "token": "def456uvw"}
]

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Auth Service</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 2em; background: #f9f9f9; font-size: 1.2rem; }
        h1 { color: #333; }
        button { padding: 12px 24px; margin: 8px; font-size: 1rem; cursor: pointer; }
        table, th, td { border: 1px solid #aaa; border-collapse: collapse; padding: 8px; }
    </style>
</head>
<body>
    <h1>Auth Service</h1>
    <p><strong>Status:</strong> Auth Service running!</p>

    <table>
        <tr><th>User</th><th>Token</th></tr>
        {% for t in tokens %}<tr><td>{{ t.user }}</td><td>{{ t.token }}</td></tr>{% endfor %}
    </table>
    <br>
    <button onclick="window.location.href='http://product.my-namespace.local:3001/product'">Go to Product</button>
    <button onclick="window.location.href='http://user.my-namespace.local:3002/user'">Go to User</button>
</body>
</html>
"""

@app.route('/auth')
def auth_root():
    return render_template_string(TEMPLATE, tokens=TOKENS)

@app.route('/')
def home():
    return render_template_string(TEMPLATE, tokens=TOKENS)

@app.route('/auth/health')
def health():
    return "ok", 200

@app.route('/login')
def login():
    return jsonify({"token": "dummy-jwt-token"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3003)
