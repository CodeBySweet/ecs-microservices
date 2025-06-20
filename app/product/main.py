from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Product Service running!"})

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3001)
    
@app.route('/product/internal-test')
def product_internal_test():
    try:
        auth_health = requests.get("http://auth.my-namespace.local:3003/auth/health").text
        user_resp = requests.get("http://user.my-namespace.local:3002/user/products").json()
        return jsonify({
            "auth_status": auth_health,
            "user_data": user_resp
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
