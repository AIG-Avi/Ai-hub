import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_ORIGINS = ["http://localhost:5000", "http://127.0.0.1:5000"]
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-jwt-secret')
    GOOGLE_API_KEY = 'YOUR_GOOGLE_API_KEY'
    GOOGLE_CX = 'YOUR_GOOGLE_CX'
