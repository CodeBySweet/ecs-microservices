from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
]

@app.route('/user')
def home():
    TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>User Service</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 2em; background: #f0f4f8; font-size: 1.2rem; color: #333; }
            h1 { color: #007acc; }
            table, th, td { border: 1px solid #ddd; border-collapse: collapse; padding: 8px; }
            table { background: #fff; box-shadow: 0 0 10px rgba(0,0,0,0.05); }
            th { background-color: #f7f7f7; }
            .nav-buttons { margin-top: 2em; }
            .btn { padding: 10px 16px; margin: 5px; border: none; background: #007acc; color: white; border-radius: 5px; text-decoration: none; font-weight: bold; }
            .btn:hover { background: #005f99; }
        </style>
    </head>
    <body>
        <h1>👤 User Service</h1>
        <p><strong>Status:</strong> User service is running independently.</p>

        <h2>User List</h2>
        <table>
            <tr><th>ID</th><th>Name</th></tr>
            {% for u in users %}
                <tr><td>{{ u.id }}</td><td>{{ u.name }}</td></tr>
            {% endfor %}
        </table>

        <div class="nav-buttons">
            <a href="http://my-app-alb-712428745.us-east-1.elb.amazonaws.com/auth" class="btn">➡️ Go to Auth</a>
            <a href="http://my-app-alb-712428745.us-east-1.elb.amazonaws.com/product" class="btn">➡️ Go to Product</a>
        </div>
    </body>
    </html>
    """
    return render_template_string(TEMPLATE, users=users)

@app.route('/user/products')
def get_products():
    return jsonify(users)

@app.route('/user/health')
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3002)
