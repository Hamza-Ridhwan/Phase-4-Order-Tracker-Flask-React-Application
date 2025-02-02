from config import create_app, db
from flask import jsonify

app = create_app()


# @app.route('/')
# def home():
#     return jsonify({'message': 'Welcome to the Order Tracker API'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)