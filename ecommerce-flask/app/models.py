from secrets import token_hex
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

cart = db.Table('cart', 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    apitoken = db.Column(db.String, default=None, nullable=True)
    cart = db.relationship("Item",
        secondary = cart,
        backref = 'cart_users',
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

    def getCart(self):
        list_of_tuples = db.session.query(cart).filter(cart.c.user_id ==self.id).all()
        return [Item.query.get(t[1]) for t in list_of_tuples]

    def saveToDB(self):
        db.session.commit()

    def addToCart(self, item):
        self.cart.append(item)
        db.session.commit()

    def removeFromCart(self, item):
        self.cart.remove(item)
        db.session.commit()


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Numeric(10,2))
    description = db.Column(db.String)
    img_url = db.Column(db.String)

    def __init__(self, name, price, desc, img):
        self.item_name = name
        self.price = price
        self.description = desc
        self.img_url = img

    def to_dict(self):
        return {
            'id': self.id,
            'item_name': self.item_name,
            'price': self.price,
            'description': self.description,
            'img_url': self.img_url
        }
