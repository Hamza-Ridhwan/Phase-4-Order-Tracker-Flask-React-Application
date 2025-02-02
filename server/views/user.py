from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import db
from models import User, Order

user_blueprint = Blueprint('user', __name__)

# -------------------- Get Profile --------------------
@user_blueprint.route('/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify(user.to_json()), 200

# -------------------- Update Profile --------------------
@user_blueprint.route('/profile_update', methods=['PUT'])
@jwt_required()
def update_user_profile():
    user_id = get_jwt_identity()
    data = request.get_json()

    # Log the received data
    print("Received update data:", data)

    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if not first_name and not last_name:
        return jsonify({'message': 'At least one field (first_name or last_name) must be provided for update'}), 400

    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name

    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'}), 200


# -------------------- Delete Profile (With Confirmation) --------------------
@user_blueprint.route('/profile_delete', methods=['DELETE'])
@jwt_required()
def delete_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()
    if not data.get('confirm') or data['confirm'].lower() != 'yes':
        return jsonify({'message': 'You must confirm deletion by setting "confirm": "yes"'}), 400

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'Profile deleted successfully'}), 200
