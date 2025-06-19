from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Auth Service running!"})

@app.route('/login')
def login():
    return jsonify({"token": "dummy-jwt-token"})

@app.route('/health')
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
