from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from flask_mail import Mail 
import os
from dotenv import load_dotenv 

# Load environment variables from .env file
load_dotenv()

# Initialize extensions
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
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com') 
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'  
    app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'False') == 'True'  
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'hamzathehamzah@gmail.com')

    # Initialize Extensions
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)  
    migrate = Migrate(app, db)

    # Register Blueprints
    from views import auth_blueprint, order_blueprint, shipment_blueprint, user_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(order_blueprint, url_prefix='/order')
    app.register_blueprint(shipment_blueprint, url_prefix='/shipment')
    app.register_blueprint(user_blueprint, url_prefix='/user')

    return app
