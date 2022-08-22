from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required
from ..apiauthhelper import token_required
from app.shop.forms import ItemForm
from app.models import Items, User, db, Cart


shop = Blueprint('shop', __name__, template_folder='shoptemplates')

@shop.route('/shop', methods=["GET", "POST"])
def goToShop():
    item = Items.query.all()
    return render_template('showshop.html', item=item)

@shop.route('/cart', methods=["GET", "POST"])
def goToCart():
    user = User.query.get(current_user.id)
    cart = user.cart.all()
    total_price = 0 # unboundlocalerror occurs if not added
    for each in cart:
        total_price += int(each.price)
    total = len(cart) # shows total amount of items in cart
    return render_template('cart.html', cart=cart, total=total, total_price=total_price)

@shop.route('/add/<string:name>')
@login_required
def addToCart(name):
    item = Items.query.filter_by(name=name).first()
    current_user.cart.append(item)
    db.session.commit()
    flash('Item added to cart.', 'success')
    return redirect(url_for('shop.goToCart'))

@shop.route('/remove/<string:name>')
@login_required
def removeFromCart(name):
    item = Items.query.filter_by(name=name).first()
    current_user.cart.remove(item)
    db.session.commit()
    flash('Item removed from cart.', 'success')
    return redirect(url_for('shop.goToCart'))

@shop.route('/remove')
@login_required
def emptyCart():
    item = Items.query.all()
    for i in item:
        if i in current_user.cart:
            current_user.cart.remove(i)
            db.session.commit()
    flash('You have no items in your cart.', 'success')
    return redirect(url_for('shop.goToCart'))

# look at one product in particular
@shop.route('/shop/<int:items_id>')
def viewItem(items_id):
    item = Items.query.get(items_id)
    return render_template('singleitem.html', item=item)

@shop.route('/items/create', methods=["GET","POST"])
@login_required
def createItem():
    form = ItemForm()
    if request.method == "POST":
        if form.validate():
            title = form.title.data
            price = form.price.data
            description = form.description.data
            img_url = form.img_url.data

            item = Items(title, price, description, img_url)
            item.saveItems()
            flash('Successfully created item.', 'success')
        else:
            flash('Invalid form. Please fill out the form correctly.', 'danger')
    return render_template('createitem.html', form=form)

###### API ROUTE ######
@shop.route('/api/items/create', methods=["POST"])
@token_required
def createItemsAPI(user):
    data = request.json
    
    title = data['title']
    price = data['price']
    description = data['description']
    imgUrl = data['imgUrl']

    item = Items(title, price, description, imgUrl, user.id)
    item.saveItems()

    return {
        'status': 'ok',
        'message': "Item listed successfully."
    }

@shop.route('/api/items')
def getAllItemsAPI():
    items = Items.query.all()
    my_items = [i.to_dict() for i in items]
    return {'status': 'ok', 'total_results': len(items), "items": my_items}

@shop.route('/api/items/<int:items_id>')
def getSingleItemsAPI(items_id):
    item = Items.query.get(items_id)
    if item:
        return {
            'status': 'ok',
            'total_results': 1,
            'item': item.to_dict()
        }
    else:
        return {
            'status': 'not ok',
            'message': f"An item with the id: {items_id} does not exist."
        }

@shop.route('/api/cart')
@token_required
def getCartItemsAPI(user):
    cart = Cart.query.filter_by(user_id=user.id).all()
    print(cart)

    incart = [c.to_dict() for c in cart]
    items = []
    total = 0
    for each in cart:
        item = Items.query.get(each.items_id)
        items.append(item)
    incart = [i.to_dict() for i in items]
    if incart:
        return {
            'status': 'ok',
            'total_amount': len(cart),
            'items': incart
        }


@shop.route('/api/cart/add', methods=["POST"])
@token_required
def addToCartAPI(user):
    data = request.json

    title=data['title']
    items = Items.query.filter_by(title=title).first()

    incart = Cart(items.id, user.id)
    incart.save()

    return {
        'status': 'ok',
        'message': 'item added to cart'
    }
    

@shop.route('/api/cart/remove', methods=["POST"])
@token_required
def removeFromCartAPI(user):
    data = request.json
    title = data['title']

    items = Items.query.filter_by(title=title).first()
    incart = Cart.query.filter_by(user_idi=user.id, items_id=items.id).first()
    incart.delete()

    return {
        'status': 'ok',
        'message': "Item removed from cart."
    }


@shop.route('/api/cart/removeall')
@token_required
def emptyCartAPI(user):
    incart = Cart.query.filter_by(user_id=user.id).all()
    for i in incart:
        i.delete()

    return {
        'status': 'ok',
        'message': "Cart emptied."
    }