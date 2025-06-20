from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "User Service running!"})

@app.route('/user/products')
def get_products():
    return jsonify([
        {"id": 1, "name": "Laptop"},
        {"id": 2, "name": "Headphones"}
    ])

@app.route('/user/health')
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3002)
    
@app.route('/user/internal-test')
def user_internal_test():
    try:
        auth_health = requests.get("http://auth.my-namespace.local:3003/auth/health").text
        product_resp = requests.get("http://product.my-namespace.local:3001/product/products").json()
        return jsonify({
            "auth_status": auth_health,
            "product_data": product_resp
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
