from flask import Flask, jsonify, render_template_string
import requests

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Auth Service</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 2em; background: #f9f9f9; }
        h1 { color: #333; }
        button { padding: 10px 20px; margin: 5px; font-size: 1rem; }
        pre { background: #eee; padding: 1em; overflow-x: auto; }
    </style>
</head>
<body>
    <h1>Auth Service</h1>
    <p><strong>Status:</strong> Auth Service running!</p>
    
    <button onclick="window.location.href='/login'">Login (GET Token)</button>
    <button onclick="fetchTest()">Run Internal Test</button>
    
    <pre id="output">Click "Run Internal Test" to fetch data from Product and User services.</pre>
    
    <script>
    function fetchTest() {
        fetch('/auth/internal-test')
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

@app.route('/auth')
def auth_root():
    return render_template_string(TEMPLATE)

@app.route('/')
def home():
    return render_template_string(TEMPLATE)

@app.route('/auth/health')
def health():
    return "ok", 200

@app.route('/login')
def login():
    return jsonify({"token": "dummy-jwt-token"})

@app.route('/auth/internal-test')
def auth_internal_test():
    try:
        product_resp = requests.get("http://product.my-namespace.local:3001/product/products", timeout=3).json()
        user_resp = requests.get("http://user.my-namespace.local:3002/user/products", timeout=3).json()
        return jsonify({
            "status": "success",
            "product_data": product_resp,
            "user_data": user_resp
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3003)
