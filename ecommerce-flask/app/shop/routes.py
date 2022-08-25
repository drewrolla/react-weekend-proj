from flask import Blueprint, request
from ..apiauthhelper import token_required
from app.models import User, Item, cart


shop = Blueprint('shop', __name__)


@shop.route('/api/items')
def getAllItemss():
    items = Item.query.all()
    return {
        'status': 'ok',
        'items': [i.to_dict() for i in items] 
    }


@shop.route('/api/items/<int:item_id>')
def getOneProduct(item_id):
    item = Item.query.get(item_id)
    return {
        'status': 'ok',
        'item': item.to_dict()
    }


@shop.route('/api/cart')
@token_required
def getCart(user):
    return {
        'status': 'ok',
        'cart': [i.to_dict() for i in user.getCart()]
        }


@shop.route('/api/cart/add', methods=["POST"])
@token_required
def addToCart(user):
    data = request.json
    item_id = data['itemId']
    item = Item.query.get(item_id)
    user.addToCart(item)
    return {
        'status': 'ok',
        'message': 'Item added to cart.'
        }


@shop.route('/api/cart/remove', methods=["POST"])
@token_required
def removeFromCart(user):
    data = request.json
    item_id = data['itemId']
    item = Item.query.get(item_id)
    user.removeFromCart(item)
    return {
        'status':'ok', 
        'message':'Item removed from cart.'
        }