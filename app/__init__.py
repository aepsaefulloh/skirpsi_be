from flask import Flask
from app.routes import init_routes
from app.database import init_db

def create_app():
    app = Flask(__name__)
    init_routes(app)
    init_db()  # Initialize database
    return app