from faker import Faker
from config import db, create_app
from models import User, Order, Shipment
from werkzeug.security import generate_password_hash
import random

app = create_app()
fake = Faker()

# Number of records to create
number_of_users = 10
number_of_orders = 20

with app.app_context():
    db.drop_all()
    db.create_all()

    # Create Users
    users = []
    for _ in range(number_of_users):
        hashed_password = generate_password_hash(fake.password())
        user = User(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.unique.email(),
            password=hashed_password  # Store hashed password
        )
        db.session.add(user)
        users.append(user)
    db.session.commit()

    # Create Orders
    orders = []
    statuses = ['pending', 'shipped', 'delivered']
    for _ in range(number_of_orders):
        order = Order(
            user_id=random.choice(users).id,
            product=fake.word(),
            status=random.choice(statuses)
        )
        db.session.add(order)
        orders.append(order)
    db.session.commit()

    # Create Shipments (one per order, only if shipped or delivered)
    for order in orders:
        if order.status in ['shipped', 'delivered']:
            shipped_date = fake.date_time_this_year()
            delivery_date = None
            if order.status == 'delivered':
                delivery_date = fake.date_time_this_year()

            shipment = Shipment(
                order_id=order.id,
                tracking_number=fake.uuid4(),
                shipped_date=shipped_date,
                delivery_date=delivery_date
            )
            db.session.add(shipment)
    db.session.commit()

    # Add Ratings and Reviews to Delivered Orders
    for order in orders:
        if order.status == 'delivered':
            rating = random.randint(1, 5)  # Random rating between 1 and 5
            review = fake.sentence(nb_words=10)  # Random review text
            order.rating = rating
            order.review = review
            db.session.commit()

    print("Database seeded successfully!")
