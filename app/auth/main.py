from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Auth Service running!"})

@app.route('/auth/health')
def health():
    return "ok", 200

@app.route('/login')
def login():
    return jsonify({"token": "dummy-jwt-token"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3003)

@app.route('/auth/internal-test')
def auth_internal_test():
    try:
        product_resp = requests.get("http://product.my-namespace.local:3001/product/products").json()
        user_resp = requests.get("http://user.my-namespace.local:3002/user/products").json()
        return jsonify({
            "product_data": product_resp,
            "user_data": user_resp
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
