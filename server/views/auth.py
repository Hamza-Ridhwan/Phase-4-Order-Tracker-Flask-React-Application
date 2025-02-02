from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from models import User
from flask_mail import Message 
from config import db, mail  
import re
import os

# Blueprint
auth_blueprint = Blueprint('auth', __name__)

# -------------------- Helper Functions --------------------
def is_valid_email(email):
    """Validate email format."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_password(password):
    """Ensure password meets security standards."""
    return len(password) >= 8 and any(char.isdigit() for char in password)

# -------------------- Sign up as a User --------------------
@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    if not is_valid_email(data['email']):
        return jsonify({'message': 'Invalid email format'}), 400

    if not is_valid_password(data['password']):
        return jsonify({'message': 'Password must be at least 8 characters long and include a number'}), 400

    # Check if email is already registered
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'message': 'Email already registered'}), 400 

    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=new_user.id)

    return jsonify({
        'access_token': access_token,
        'message': 'User created successfully'
    }), 201

# -------------------- Login as a User --------------------
@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            },
            'message': 'Login successful'
        }), 200

    return jsonify({'message': 'Invalid credentials'}), 401

# -------------------- Logout as a User --------------------
@auth_blueprint.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({'message': 'Logged out successfully'}), 200

# ------------------ Change Password ------------------
@auth_blueprint.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data.get('old_password') or not data.get('new_password'):
        return jsonify({'message': 'Both old and new passwords are required'}), 400

    if not is_valid_password(data['new_password']):
        return jsonify({'message': 'New password must be at least 8 characters long and include a number'}), 400

    user = User.query.get(user_id)

    if not user or not check_password_hash(user.password, data['old_password']):
        return jsonify({'message': 'Incorrect old password'}), 401

    user.password = generate_password_hash(data['new_password'], method='pbkdf2:sha256')
    db.session.commit()

    return jsonify({'message': 'Password changed successfully'}), 200

# -------------------- Password Reset --------------------
@auth_blueprint.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'message': 'Email is required'}), 400

    # Check if email exists
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'No user found with that email'}), 404

    # Generate a token for password reset
    reset_token = create_access_token(identity=user.id)

    # Create the reset password URL (this could be a URL for your frontend to process)
    reset_url = f"{os.getenv('FRONTEND_URL')}/reset-password/{reset_token}"

    # Create the reset email message
    msg = Message('Password Reset Request', recipients=[email])
    msg.body = f"To reset your password, click the following link: {reset_url}"
    msg.html = f"<p>To reset your password, <a href='{reset_url}'>click here</a>.</p>"

    # Send the email
    try:
        mail.send(msg)
        return jsonify({'message': 'Password reset email sent successfully.'}), 200
    except Exception as e:
        return jsonify({'message': f'Failed to send email: {str(e)}'}), 500

# ------------------ Protected Route (for testing JWT) ------------------
@auth_blueprint.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify({'message': 'This is a protected route.'}), 200
