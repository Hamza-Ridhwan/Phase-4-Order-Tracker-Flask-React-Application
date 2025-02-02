from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import db
from models import Shipment, Order

shipment_blueprint = Blueprint('shipment', __name__)

# -------------------- Track Order by Tracking Number --------------------
@shipment_blueprint.route('/shipment/<string:tracking_number>', methods=['GET'])
@jwt_required()
def track_order(tracking_number):
    user_id = get_jwt_identity()

    shipment = Shipment.query.filter_by(tracking_number=tracking_number).first()
    
    if not shipment:
        return jsonify({'message': 'Shipment not found'}), 404

    # Ensure the user owns the order linked to this shipment
    order = Order.query.filter_by(id=shipment.order_id, user_id=user_id).first()
    if not order:
        return jsonify({'message': 'Unauthorized to track this shipment'}), 403

    return jsonify(shipment.to_json()), 200

# -------------------- Get Shipment Details by Order ID --------------------
@shipment_blueprint.route('/shipment/order/<int:order_id>', methods=['GET'])
@jwt_required()
def get_shipment_by_order(order_id):
    user_id = get_jwt_identity()
    
    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    if not order:
        return jsonify({'message': 'Order not found or unauthorized'}), 404

    shipment = Shipment.query.filter_by(order_id=order_id).first()
    if not shipment:
        return jsonify({'message': 'No shipment found for this order'}), 200  

    return jsonify(shipment.to_json()), 200
