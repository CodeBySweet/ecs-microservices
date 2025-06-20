from flask import Flask, jsonify, render_template_string
import requests

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Product Service</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 2em; background: #f5f5f5; }
        h1 { color: #2a2a2a; }
        button { padding: 10px 15px; margin: 8px; font-size: 1rem; }
        pre { background: #eee; padding: 1em; white-space: pre-wrap; }
    </style>
</head>
<body>
    <h1>Product Service</h1>
    <button onclick="window.location.href='/product/products'">View Products</button>
    <button onclick="fetchTest()">Run Internal Test</button>
    <pre id="output">Click "Run Internal Test" to fetch data from Auth and User services.</pre>

    <script>
    function fetchTest() {
        fetch('/product/internal-test')
            .then(resp => resp.json())
            .then(data => {
                document.getElementById('output').textContent = JSON.stringify(data, null, 2);
            })
            .catch(err => {
                document.getElementById('output').textContent = 'Error: ' + err;
            });
    }
    </script>
</body>
</html>
"""

@app.route('/')
@app.route('/product')
def home():
    return render_template_string(TEMPLATE)

@app.route('/')
def home():
    return render_template_string(TEMPLATE)

@app.route('/product/products')
def get_products():
    return jsonify([
        {"id": 1, "name": "Laptop"},
        {"id": 2, "name": "Smartphone"},
        {"id": 3, "name": "Headphones"}
    ])

@app.route('/product/health')
def health():
    return "ok", 200

@app.route('/product/internal-test')
def product_internal_test():
    try:
        auth_health = requests.get("http://auth.my-namespace.local:3003/auth/health", timeout=3).text
        user_resp = requests.get("http://user.my-namespace.local:3002/user/products", timeout=3).json()
        return jsonify({
            "status": "success",
            "auth_status": auth_health,
            "user_data": user_resp
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3001)
