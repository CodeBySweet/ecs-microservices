from flask import Flask, jsonify, render_template_string
import requests

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>User Service</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 2em; background: #fff9c4; }
        h1 { color: #f9a825; }
        button { padding: 10px 15px; margin: 8px; font-size: 1rem; }
        pre { background: #eee; padding: 1em; white-space: pre-wrap; }
    </style>
</head>
<body>
    <h1>Welcome to the User Service</h1>
    <button onclick="window.location.href='/user/products'">View User Products</button>
    <button onclick="fetchTest()">Run Internal Test</button>
    <pre id="output">Click "Run Internal Test" to fetch data from Auth and Product services.</pre>

    <script>
    function fetchTest() {
        fetch('/user/internal-test')
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
@app.route('/user')
def home():
    return render_template_string(TEMPLATE)

@app.route('/user/products')
def get_products():
    return jsonify({
        "message": "This is the User Service showing user-associated products",
        "products": [
            {"id": 1, "name": "Laptop"},
            {"id": 2, "name": "Headphones"}
        ]
    })

@app.route('/user/health')
def health():
    return "ok", 200

@app.route('/user/internal-test')
def user_internal_test():
    try:
        auth_health = requests.get("http://auth.my-namespace.local:3003/auth/health", timeout=3).text
        product_resp = requests.get("http://product.my-namespace.local:3001/product/products", timeout=3).json()
        return jsonify({
            "status": "success",
            "auth_status": auth_health,
            "product_data": product_resp
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3002)
