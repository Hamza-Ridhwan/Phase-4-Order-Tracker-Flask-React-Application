from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from flask_mail import Mail  # Import Flask-Mail
import os

db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()  # Initialize Flask-Mail

def create_app():
    app = Flask(__name__)

    # App Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///order_tracker.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', '98734jksakjh jhgsd908asd')

    # Flask-Mail Configuration
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')  # You can change this to your email provider
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT', 587)
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False  # Set to True for SSL instead of TLS
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Email address
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Email password or app-specific password
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'no-reply@yourdomain.com')

    # Initialize Extensions
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)  # Initialize Flask-Mail
    migrate = Migrate(app, db)

    # Register Blueprints
    from views import auth_blueprint, order_blueprint, shipment_blueprint, user_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(order_blueprint, url_prefix='/order')
    app.register_blueprint(shipment_blueprint, url_prefix='/shipment')
    app.register_blueprint(user_blueprint, url_prefix='/user')

    return app
