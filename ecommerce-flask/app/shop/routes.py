from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required
from ..apiauthhelper import token_required
from app.shop.forms import ItemForm
from app.models import Items, db, User


shop = Blueprint('shop', __name__, template_folder='shoptemplates')


# @shop.route('/items/create', methods=["GET","POST"])
# @login_required
# def createItem():
#     form = ItemForm()
#     if request.method == "POST":
#         if form.validate():
#             title = form.title.data
#             img_url = form.img_url.data
#             caption = form.caption.data

#             item = Items(title, img_url, caption, current_user.id)
#             item.save()
#             flash('Successfully created item.', 'success')
#         else:
#             flash('Invalid form. Please fill out the form correctly.', 'danger')
#     return render_template('createitem.html', form=form)

@shop.route('/items')
def getAllItems():
    items = Items.query.order_by(Items.date_created.desc()).all()
    return render_template('showshop.html', items=items)


@shop.route('/items/<int:item_id>')
def getSingleItem(item_id):
    item = Items.query.get(item_id)
    # item = Items.query.filter_by(id=item_id).first()
    return render_template('singleitem.html', item=item)

# @shop.route('/items/update/<int:item_id>', methods=["GET", "POST"])
# @login_required
# def updateItem(item_id):
#     form = ItemForm()
#     # item = Items.query.get(item_id)
#     item = Items.query.filter_by(id=item_id).first()
#     if current_user.id != item.user_id:
#         flash('You are not allowed to update another user\'s items.', 'danger')
#         return redirect(url_for('shop.getSingleItem', item_id=item_id))
#     if request.method=="POST":
#         if form.validate():
#             title = form.title.data
#             img_url = form.img_url.data
#             caption = form.caption.data

#             item.updateItemInfo(title,img_url,caption)
#             item.saveUpdates()
#             flash('Successfully updated item.', 'success')
#             return redirect(url_for('shop.getSingleItem', item_id=item_id))
#         else:
#             flash('Invalid form. Please fill out the form correctly.', 'danger')
#     return render_template('updateitem.html', form=form,  item=item)


# @shop.route('/items/delete/<int:item_id>')
# @login_required
# def deleteItem(item_id):
#     item = Items.query.get(item_id)
#     if current_user.id != item.user_id:
#         flash('You are not allowed to delete another user\'s items.', 'danger')
#         return redirect(url_for('shop.getSingleItem', item_id=item_id))
#     item.delete()
#     flash('Successfully delete item.', 'success')
#     return redirect(url_for('shop.getAllItems'))


# @shop.route('/follow/<int:user_id>')
# @login_required
# def followUser(user_id):
#     user = User.query.get(user_id)
#     current_user.follow(user)
#     return redirect(url_for('index'))

# @shop.route('/unfollow/<int:user_id>')
# @login_required
# def unfollowUser(user_id):
#     user = User.query.get(user_id)
#     current_user.unfollow(user)
#     return redirect(url_for('index'))





################# API ROUTES #####################
@shop.route('/api/items')
def getAllItemsAPI():
    # args = request.args
    # pin = args.get('pin')
    # print(pin, type(pin))
    # if pin == '1234':

        items = Items.query.order_by(Items.date_created.desc()).all()

        my_items = [i.to_dict() for i in items]
        return {'status': 'ok', 'total_results': len(items), "items": my_items}
    # else:
    #     return {
    #         'status': 'not ok',
    #         'code': 'Invalid Pin',
    #         'message': 'The pin number was incorrect, please try again.'
    #     }

@shop.route('/api/items/<int:item_id>')
def getSingleItemAPI(item_id):
    item = Items.query.get(item_id)
    if item:
        return {
            'status': 'ok',
            'total_results': 1,
            "item": item.to_dict()
            }
    else:
        return {
            'status': 'not ok',
            'message': f"A item with the id : {item_id} does not exist."
        }


@shop.route('/api/items/create', methods=["POST"])
@token_required
def createItemAPI(user):
    data = request.json # this is coming from POST request Body

    title = data['title']
    caption = data['caption']
    img_url = data['imgUrl']

    item = Items(title, img_url, caption, user.id)
    item.save()

    return {
        'status': 'ok',
        'message': "Items was successfully created."
    }

@shop.route('/api/items/update', methods=["POST"])
@token_required
def updateItemAPI(user):
    data = request.json # this is coming from POST request Body

    item_id = data['itemId']

    item = Items.query.get(item_id)
    if item.user_id != user.id:
        return {
            'status': 'not ok',
            'message': "You cannot update another user's item!"
        }

    title = data['title']
    caption = data['caption']
    img_url = data['imgUrl']

    item.updateItemInfo(title, img_url, caption)
    item.saveUpdates()

    return {
        'status': 'ok',
        'message': "Items was successfully updated."
    }

