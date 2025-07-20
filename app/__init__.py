# app/__init__.py
from flask import Flask
from app.routes import init_routes
from app.database import init_db
from app.utils.csv_to_db import insert_csv_to_db
from app.utils.train_knn_from_csv import train_knn_from_csv

def create_app():
    app = Flask(__name__)
    init_routes(app)
    init_db()  
    insert_csv_to_db()
    train_knn_from_csv() 
    return app
