from secrets import token_hex
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

fake_shop = db.Table('fake_shop',
    db.Column('cart_id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('items_id', db.Integer, db.ForeignKey('items.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    apitoken = db.Column(db.String, default=None, nullable=True)
    cart = db.relationship("Items",
        secondary = fake_shop,
        backref = 'buyer',
        lazy = 'dynamic'
    )

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.apitoken = token_hex(16)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'token': self.apitoken
        }

    def saveToDB(self):
        db.session.commit()


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    description = db.Column(db.String)
    img_url = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, price, description, img_url, user_id):
        self.name = name
        self.price = price
        self.description = description
        self.img_url = img_url
        self.user_id = user_id

    def saveItems(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'img_url': self.img_url,
            'user_id': self.user_id
        }

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    items_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)

    def __init__(self, user_id, items_id):
        self.user_id = user_id
        self.items_id = items_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'items_id': self.items_id
        }