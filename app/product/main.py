from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "Product Service running!",
        "routes": {
            "Product List": "/product/products",
            "Health Check": "/product/health",
            "Internal Test": "/product/internal-test"
        }
    })

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
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3001)
