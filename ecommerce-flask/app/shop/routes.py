from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required
from ..apiauthhelper import token_required
from app.shop.forms import ItemForm
from app.models import Items, db, User


shop = Blueprint('shop', __name__, template_folder='shoptemplates')


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
            item.save()
            flash('Successfully created item.', 'success')
        else:
            flash('Invalid form. Please fill out the form correctly.', 'danger')
    return render_template('createitem.html', form=form)

@shop.route('/items')
def getAllItems():
    items = Items.query.all
    return render_template('showshop.html', items=items)


@shop.route('/items/<int:item_id>')
def getSingleItem(item_id):
    item = Items.query.get(item_id)
    # item = Items.query.filter_by(id=item_id).first()
    return render_template('singleitem.html', item=item)


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


# ################# API ROUTES #####################
# @shop.route('/api/items')
# def getAllItemsAPI():
#     # args = request.args
#     # pin = args.get('pin')
#     # print(pin, type(pin))
#     # if pin == '1234':

#         items = Items.query.order_by(Items.date_created.desc()).all()

#         my_items = [i.to_dict() for i in items]
#         return {'status': 'ok', 'total_results': len(items), "items": my_items}
#     # else:
#     #     return {
#     #         'status': 'not ok',
#     #         'code': 'Invalid Pin',
#     #         'message': 'The pin number was incorrect, please try again.'
#     #     }

# @shop.route('/api/items/<int:item_id>')
# def getSingleItemAPI(item_id):
#     item = Items.query.get(item_id)
#     if item:
#         return {
#             'status': 'ok',
#             'total_results': 1,
#             "item": item.to_dict()
#             }
#     else:
#         return {
#             'status': 'not ok',
#             'message': f"A item with the id : {item_id} does not exist."
#         }


# @shop.route('/api/items/create', methods=["POST"])
# @token_required
# def createItemAPI(user):
#     data = request.json # this is coming from POST request Body

#     title = data['title']
#     price = data['price']
#     description = data['description']
#     img_url = data['imgUrl']

#     item = Items(title, price, description, img_url, user.id)
#     item.save()

#     return {
#         'status': 'ok',
#         'message': "Items was successfully created."
#     }

# @shop.route('/api/items/update', methods=["POST"])
# @token_required
# def updateItemAPI(user):
#     data = request.json # this is coming from POST request Body

#     item_id = data['itemId']

#     item = Items.query.get(item_id)
#     if item.user_id != user.id:
#         return {
#             'status': 'not ok',
#             'message': "You cannot update another user's item!"
#         }

#     title = data['title']
#     price = data['price']
#     description = data['description']
#     img_url = data['imgUrl']

#     item.updateItemInfo(title, price, description, img_url)
#     item.saveUpdates()

#     return {
#         'status': 'ok',
#         'message': "Items was successfully updated."
#     }

