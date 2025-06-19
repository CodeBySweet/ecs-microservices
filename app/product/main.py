from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "User Service running!"})

@app.route('/user/<user_id>')
def get_user(user_id):
    return jsonify({"id": user_id, "name": "John Doe"})

@app.route('/health')
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
