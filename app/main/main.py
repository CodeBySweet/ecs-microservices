from flask import Flask, render_template_string
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    services = {
        "Auth Service": "http://my-app-alb-712428745.us-east-1.elb.amazonaws.com/auth",
        "Product Service": "http://my-app-alb-712428745.us-east-1.elb.amazonaws.com/product",
        "User Service": "http://my-app-alb-712428745.us-east-1.elb.amazonaws.com/user"
    }

    health_endpoints = {
        "Auth Service": "http://my-app-alb-712428745.us-east-1.elb.amazonaws.com/auth/health",
        "Product Service": "http://my-app-alb-712428745.us-east-1.elb.amazonaws.com/product/health",
        "User Service": "http://my-app-alb-712428745.us-east-1.elb.amazonaws.com/user/health"
    }

    health = {}
    for name, url in health_endpoints.items():
        try:
            status = requests.get(url, timeout=2).text
        except Exception as e:
            status = f"Unavailable ({e})"
        health[name] = status

    last_checked = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

    TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Microservices Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f3f3f3; padding: 2em; font-size: 1.3rem; }
            h1 { color: #333; }
            ul { list-style: none; padding: 0; }
            li { margin-bottom: 1em; }
            a { color: #0066cc; text-decoration: none; font-weight: bold; }
            .status { color: green; }
            .status.error { color: red; }
            .timestamp { margin-top: 1em; font-size: 0.9rem; color: #555; }
        </style>
    </head>
    <body>
        <h1>Microservices Demo Dashboard</h1>
        <ul>
            {% for name, url in services.items() %}
                <li>
                    <a href="{{ url }}" target="_blank">{{ name }}</a>
                    <span class="status {% if 'ok' not in health[name] %}error{% endif %}"> - {{ health[name] }}</span>
                </li>
            {% endfor %}
        </ul>
        <p class="timestamp">Last checked: {{ last_checked }}</p>
    </body>
    </html>
    """
    return render_template_string(TEMPLATE, services=services, health=health, last_checked=last_checked)

@app.route('/main/health')
def health_check():
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3004)
