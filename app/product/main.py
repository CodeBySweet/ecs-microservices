from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "User Service running!"})

@app.route('/product/products')
def get_products(user_id):
    return jsonify({"id": user_id, "name": "John Doe"})

@app.route('/product/health')
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3001)
