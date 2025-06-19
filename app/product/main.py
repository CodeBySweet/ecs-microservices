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