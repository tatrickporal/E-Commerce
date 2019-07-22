# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

import datetime

class Post(object):
    """Simple class to create synthetic posts"""
    def __init__(self):
        pass

@auth.requires_login()
def setup():
    """Deleted all products, orders, and reviews, not at all smart for production but for testing okay"""
    db(db.Product_Table).delete() 
    db(db.Product_Order).delete() 
    db(db.Product_Review).delete() 
    return "Deleted all products, orders, and reviews, not at all smart for production but for testing okay"

@auth.requires_login()
def index():
    """Home page for the website,
       Displays all products in the marketplace"""
    query = db.Product_Table
    db.Product_Table.product_owner.represent = ""
    db.Product_Table.product_name.represent = lambda  id, row: \
        A(row.product_name, _href=URL('default', 'product_page', args=[row.id]))
    rows = db(query).select().render()
    return dict(rows=rows)

@auth.requires_login()
def product_page():
    """display the product clicked"""
    form = SQLFORM.factory(db.Product_Order)

    row = db(db.Product_Table.id == request.args[0]).select().first()
    reviews_row = db(db.Product_Review.product_reference == request.args[0]).select().render()
    product_owner = db(db.auth_user.id == row.product_owner.id).select().first()
    db.Product_Review.author.represent = lambda  id, row: \
        db(db.auth_user.id == id).select().first().username
    db.Product_Order.product_owner.default = product_owner 
    db.Product_Order.product_ref.default = row

    if form.process().accepted: 
        db.Product_Order.insert(
            quantity = form.vars.quantity,
            total_order_price =  (form.vars.quantity * row.price)
        )

        redirect(URL('default', 'past_orders'))
    return dict(row=row, reviews_row=reviews_row, order_form=form, product_owner=product_owner)

@auth.requires_login()
def submit_review():
    """Submit the a review of the product given with request.args[0]"""
    product = db(db.Product_Table.id == request.args[0]).select().first()
    db.Product_Review.product_reference.default = product
    db.Product_Review.product_reference.represent = lambda  id, row: \
        A(product.product_name, _href=URL('default', 'product_page', args=[product.id]))
    db.Product_Review.product_reference.label = "Your review describes this product"
    form = SQLFORM(db.Product_Review)
    
    if form.process().accepted:
        tpr = product.total_possible_ratings
        tr = product.total_ratings
        ts = product.total_stock
        ar = ((tr+form.vars.score)/(tpr+10))*100
        product.update_record(
            total_possible_ratings=tpr + 10, 
            total_ratings=form.vars.score + tr,
            avg_rating = ar,
            )
        redirect(URL('default', 'product_page', args=[product.id]))
    logger.info("My session is: %r" % session)
    return dict(form=form)

@auth.requires_login()
def past_orders():
    """Displayes all the orders of the signed in user"""
    db.Product_Order.product_buyer.represent = ""
    db.Product_Order.product_owner.represent = lambda  id, row: \
        P( db(db.Product_Order.product_owner == db.auth_user.id).select().first().auth_user.username + ", " + db(db.Product_Order.product_owner == db.auth_user.id).select().first().auth_user.email)
    db.Product_Order.product_ref.represent = lambda  id, row: \
        A( db(db.Product_Order.product_ref == db.Product_Table.id).select().first().Product_Table.product_name, _href=URL('default', 'product_page', args=[db(db.Product_Order.product_ref == db.Product_Table.id).select().first().Product_Table.id]))
   
    past_orders =  db(db.Product_Order.product_buyer == auth.user).select().render()
    
    return dict(past_orders=past_orders)


@auth.requires_login()
def sell():
    """Displays the form in which the user can add a product to the market place"""
    form = SQLFORM(db.Product_Table)
    if form.process().accepted:
        redirect(URL('default', 'index'))
    logger.info("My session is: %r" % session)
    return dict(form=form)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()