import os
import sys
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from functools import wraps

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# Import routes
from src.routes.auth import auth_bp
from src.routes.numbers import numbers_bp
from src.routes.messages import messages_bp

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(numbers_bp)
app.register_blueprint(messages_bp)

@app.route('/')
def index():
    if 'account_sid' in session and 'auth_token' in session:
        return redirect(url_for('numbers.dashboard'))
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
