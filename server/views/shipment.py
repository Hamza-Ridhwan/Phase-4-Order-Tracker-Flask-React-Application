from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import db
from models import Shipment, Order, User
from datetime import datetime

shipment_blueprint = Blueprint('shipment', __name__)

# -------------------- Create Shipment for Order --------------------
@shipment_blueprint.route('/shipment/create', methods=['POST'])
@jwt_required()
def create_shipment():
    user_id = get_jwt_identity()

    # Get user from the database
    user = User.query.filter_by(id=user_id).first()
    
    # Ensure the user is an admin by checking the is_admin field
    if not user or not user.is_admin:
        return jsonify({'message': 'Admin privileges required'}), 403

    # Get the order ID, tracking number, and delivery date from the request
    data = request.get_json()
    order_id = data.get('order_id')
    tracking_number = data.get('tracking_number')
    delivery_date_str = data.get('delivery_date')

    # Check if the order exists
    order = Order.query.filter_by(id=order_id).first()
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    # Convert delivery date from string to datetime
    delivery_date = None
    if delivery_date_str:
        try:
            delivery_date = datetime.strptime(delivery_date_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD HH:MM:SS'}), 400

    # Create a new shipment for the order with optional delivery date
    shipment = Shipment(order_id=order_id, tracking_number=tracking_number, delivery_date=delivery_date)
    db.session.add(shipment)
    db.session.commit()

    return jsonify(shipment.to_json()), 201

# -------------------- Track Order by Tracking Number --------------------
@shipment_blueprint.route('/shipment/<string:tracking_number>', methods=['GET'])
@jwt_required()
def track_order(tracking_number):
    user_id = get_jwt_identity()

    shipment = Shipment.query.filter_by(tracking_number=tracking_number).first()
    
    if not shipment:
        return jsonify({'message': 'Shipment not found'}), 404

    # Ensure the user owns the order linked to this shipment, or if the user is an admin
    order = Order.query.filter_by(id=shipment.order_id).first()
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    user = User.query.filter_by(id=user_id).first()  # Make sure user is defined here
    if not user or (order.user_id != user_id and not user.is_admin):
        return jsonify({'message': 'Unauthorized to track this shipment'}), 403

    return jsonify(shipment.to_json()), 200

# -------------------- Get Shipment Details by Order ID --------------------
@shipment_blueprint.route('/shipment/order/<int:order_id>', methods=['GET'])
@jwt_required()
def get_shipment_by_order(order_id):
    user_id = get_jwt_identity()

    user = User.query.filter_by(id=user_id).first()  # Make sure user is defined here

    # Ensure the order belongs to the user, or if the user is an admin
    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    if not order and (not user or not user.is_admin):
        return jsonify({'message': 'Order not found or unauthorized'}), 404

    shipment = Shipment.query.filter_by(order_id=order_id).first()
    if not shipment:
        return jsonify({'message': 'No shipment found for this order'}), 200  

    return jsonify(shipment.to_json()), 200
