from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import db
from models import Order, User

order_blueprint = Blueprint('order', __name__)

# -------------------- Get Orders --------------------
@order_blueprint.route('/', methods=['GET'])
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).all()
    return jsonify([order.to_json() for order in orders])

# -------------------- Create Order --------------------
@order_blueprint.route('/create_order', methods=['POST'])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    data = request.get_json()

    product = data.get('product')
    if not product:
        return jsonify({'message': 'Product name is required'}), 400

    new_order = Order(user_id=user_id, product=product, status='pending')
    db.session.add(new_order)
    db.session.commit()
    return jsonify(new_order.to_json()), 201

# -------------------- Update Order --------------------
@order_blueprint.route('/update_order/<int:order_id>', methods=['PUT'])
@jwt_required()
def update_order(order_id):
    user_id = get_jwt_identity()
    order = Order.query.get(order_id)

    if not order or order.user_id != user_id:
        return jsonify({'message': 'Order not found'}), 404

    if order.status != 'pending':
        return jsonify({'message': 'Order can only be modified before shipping'}), 400

    data = request.get_json()
    product = data.get('product')

    if product:
        order.product = product
        db.session.commit()
        return jsonify({'message': 'Order updated successfully'})
    
    return jsonify({'message': 'No changes were made'}), 400

# -------------------- Cancel Order --------------------
@order_blueprint.route('/cancel_order/<int:order_id>', methods=['PUT'])
@jwt_required()
def cancel_order(order_id):
    user_id = get_jwt_identity()
    order = Order.query.get(order_id)

    if not order or order.user_id != user_id:
        return jsonify({'message': 'Order not found'}), 404

    if order.status != 'pending':
        return jsonify({'message': 'Only pending orders can be canceled'}), 400

    order.status = 'canceled'
    db.session.commit()
    return jsonify({'message': 'Order canceled successfully'})

# -------------------- Delete Order --------------------
@order_blueprint.route('/delete_order/<int:order_id>', methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    user_id = get_jwt_identity()
    order = Order.query.get(order_id)

    if not order or order.user_id != user_id:
        return jsonify({'message': 'Order not found'}), 404

    if order.status != 'pending':
        return jsonify({'message': 'Only pending orders can be deleted'}), 400

    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted successfully'})

# -------------------- Rate Order --------------------
@order_blueprint.route('/rate_order/<int:order_id>', methods=['POST'])
@jwt_required()
def rate_order(order_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    try:
        rating = int(data.get('rating'))
    except (ValueError, TypeError):
        return jsonify({'message': 'Rating must be a valid integer between 1 and 5'}), 400

    if not (1 <= rating <= 5):
        return jsonify({'message': 'Rating must be between 1 and 5'}), 400

    order = Order.query.get(order_id)

    if not order or order.user_id != user_id:
        return jsonify({'message': 'Order not found'}), 404

    if order.status != 'delivered':
        return jsonify({'message': 'You can only rate orders that have been delivered'}), 400

    order.rating = rating
    db.session.commit()
    return jsonify({'message': 'Order rated successfully'})


# -------------------- Review Order --------------------
@order_blueprint.route('/review_order/<int:order_id>', methods=['POST'])
@jwt_required()
def review_order(order_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    review = data.get('review')
    
    if not review:
        return jsonify({'message': 'Review is required'}), 400

    order = Order.query.get(order_id)

    if not order or order.user_id != user_id:
        return jsonify({'message': 'Order not found'}), 404

    if order.status != 'delivered':
        return jsonify({'message': 'You can only review orders that have been delivered'}), 400

    order.review = review
    db.session.commit()

    return jsonify({'message': 'Order review submitted successfully'}), 200


# -------------------- Update Order Status (Admin Only) --------------------
@order_blueprint.route('/update_status/<int:order_id>', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    # Ensure the user is an admin
    if not user or not user.is_admin:
        return jsonify({'message': 'Permission denied. Admin access required.'}), 403

    order = Order.query.get(order_id)

    if not order:
        return jsonify({'message': 'Order not found'}), 404

    # Determine the allowed status transitions
    if order.status == 'pending':
        new_status = 'shipped'
    elif order.status == 'shipped':
        new_status = 'delivered'
    else:
        return jsonify({'message': 'Order has already been delivered or canceled, no further status updates are allowed.'}), 400

    order.status = new_status
    db.session.commit()

    return jsonify({'message': f'Order status updated to {new_status} successfully'}), 200
