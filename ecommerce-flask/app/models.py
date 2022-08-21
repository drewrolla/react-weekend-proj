from secrets import token_hex
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

finsta_shop = db.Table('finsta_shop',
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
        secondary = finsta_shop,
        backref = 'buyers',
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

    def __init__(self, name, price, description, img_url):
        self.name = name
        self.price = price
        self.description = description
        self.img_url = img_url

    def saveItems(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'img_url': self.img_url
        }