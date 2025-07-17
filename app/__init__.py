import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Secret key for session management and CSRF protection
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')

    # Database configuration using DATABASE_URL from environment, fallback to local PostgreSQL
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL',
        'postgresql://postgres:Cottage087@localhost:5432/glamping'
    )

    # Ensure compatibility if DATABASE_URL uses 'postgres://' instead of 'postgresql://'
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    
    # Register blueprint
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


