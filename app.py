from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
from models.models import db
from routes.home import home_bp
from routes.api import api_bp
import logging
import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import requests
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_argon2 import Argon2
from dotenv import load_dotenv
import os

# Load secrets and config from .env
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_CX = os.getenv('GOOGLE_CX')

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config.from_object(Config)
app.config['SECRET_KEY'] = SECRET_KEY
# Secure session cookies
app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JS access to cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Mitigate CSRF

# Logging
logging.basicConfig(level=logging.INFO)

# Database
db.init_app(app)

# CORS (restrict to allowed origins)
CORS(app, origins=Config.CORS_ORIGINS)

# Register blueprints
app.register_blueprint(home_bp)
app.register_blueprint(api_bp)

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_CX = os.getenv('GOOGLE_CX')

# Load FAQ knowledge base
with open('faq-data.json', 'r', encoding='utf-8') as f:
    FAQ_DATA = json.load(f)

def search_faq(question):
    question_lower = question.lower()
    for entry in FAQ_DATA:
        if entry['question'].lower() in question_lower or question_lower in entry['question'].lower():
            return entry['answer']
    return None

def query_openai_gpt4(question):
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gpt-4',
        'messages': [
            {'role': 'system', 'content': 'You are an expert AI assistant.'},
            {'role': 'user', 'content': question}
        ],
        'max_tokens': 256,
        'temperature': 0.7
    }
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=10)
        resp.raise_for_status()
        result = resp.json()
        answer = result['choices'][0]['message']['content']
        return answer
    except Exception as e:
        print('OpenAI error:', e)
        return None

def google_search(question):
    url = f'https://www.googleapis.com/customsearch/v1?q={question}&key={GOOGLE_API_KEY}&cx={GOOGLE_CX}'
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        results = []
        if 'items' in data:
            for item in data['items'][:3]:
                results.append(item.get('snippet', ''))
        if results:
            return ' '.join(results)
    except Exception as e:
        print('Google Search error:', e)
    return None

# Security: Set strict Content Security Policy, HSTS, and other headers
csp = {
    'default-src': ["'self'"],
    'script-src': ["'self'", 'https://cdn.tailwindcss.com', 'https://cdnjs.cloudflare.com'],
    'style-src': ["'self'", 'https://fonts.googleapis.com', 'https://cdnjs.cloudflare.com'],
    'img-src': ["'self'", 'data:', 'https://images.unsplash.com', 'https://cdn-icons-png.flaticon.com', 'https://upload.wikimedia.org'],
    'font-src': ["'self'", 'https://fonts.gstatic.com', 'https://cdnjs.cloudflare.com'],
}
Talisman(app, content_security_policy=csp, force_https=True, strict_transport_security=True)

# Security: Rate limiting to prevent DDoS
limiter = Limiter(app, key_func=get_remote_address, default_limits=["100 per minute"])

# Security: Argon2 password hashing helper
argon2 = Argon2(app)

# Error handling
@app.errorhandler(404)
def not_found(error):
    return {"error": "Not found"}, 404

@app.errorhandler(500)
def server_error(error):
    return {"error": "Server error"}, 500

@app.route('/chat', methods=['POST'])
@limiter.limit("10 per minute")
def chat():
    data = request.get_json()
    # Sanitize user input to prevent XSS/Injection
    question = bleach.clean(data.get('question', '').strip(), tags=[], attributes={}, styles=[], strip=True)
    if not question:
        return jsonify({'answer': 'Please enter a valid question.'})
    # 1. Search FAQ knowledge base
    answer = search_faq(question)
    if answer:
        return jsonify({'answer': answer})
    # 2. Query LLM (OpenAI GPT-4)
    answer = query_openai_gpt4(question)
    if answer and len(answer) > 10:
        return jsonify({'answer': answer})
    # 3. Fallback to Google Search
    answer = google_search(question)
    if answer:
        return jsonify({'answer': answer})
    return jsonify({'answer': 'Sorry, I could not find an answer.'})

# Example login route with stricter rate limit and password hashing
@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # Stricter limit for login
def login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    # Fetch user from DB (pseudo-code)
    # user = User.query.filter_by(username=username).first()
    # if user and argon2.check_password_hash(user.password_hash, password):
    #     # Set session, etc.
    #     return jsonify({'success': True})
    # return jsonify({'success': False}), 401
    return jsonify({'success': False, 'msg': 'Demo only'}), 401

# Security: Set additional headers for all responses
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response

if __name__ == "__main__":
    app.run(debug=True)
