import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    # --- Configuration ---
    # Set a secret key for session management and forms
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'a-default-secret-key-for-dev')

    # Set the database URI
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '..', 'app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # --- Initialize extensions with the app ---
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Tell Flask-Login which view handles logins
    login_manager.login_view = 'main.login'

    with app.app_context():
        from . import models

        # Import and register blueprints
        from . import routes
        app.register_blueprint(routes.main)

    return app
