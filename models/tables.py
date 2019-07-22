# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

import datetime

def user_representation(row):
    return A(row.first_name + ' ' + row.last_name + ', ' + row.email, _href=URL('default', 'user', args=['profile']))

def get_user():
    return None if auth.user is None else auth.user

def get_current_time():
    return datetime.datetime.utcnow()

db.define_table('Product_Table',
                Field('product_name', 'string',requires=IS_NOT_EMPTY()),
                Field('product_description', 'text',requires=IS_NOT_EMPTY(),label="Describe the product", comment="Please include details like color, model, dimensions, etc"), 
                Field('price', 'double', default=0.00, label="Price per item ($)"),
                Field('total_ratings', 'integer', default=0),
                Field('total_possible_ratings', 'integer', default=0), 
                Field('avg_rating', 'double', writable=False, default=0),
                Field('total_stock', 'integer', default=1, label="Amount of items in stock"),
                Field('product_owner', 'reference auth_user', default=get_user(), writable=False, represent=lambda row: user_representation(row), label="Product Owner (YOU)"),
                Field('date_posted', 'datetime', writable=False, default=get_current_time()),
)

db.define_table('Product_Order',
                Field('product_ref', 'reference Product_Table', writable=False),
                Field('product_buyer', 'reference auth_user', writable=False, default=get_user(), represent=lambda row: user_representation(row), label="Buyer (YOU)"), 
                Field('product_owner', 'reference auth_user', writable=False), 
                Field('quantity', 'integer', default=1),
                Field('total_order_price', 'integer',writable=False, label="Total Order Price"),
)

db.define_table('Product_Review',
                Field('author', 'reference auth_user', writable=False, default=get_user(), represent=lambda row: user_representation(row), label="Author (YOU)"), 
                Field('product_reference', 'reference Product_Table', writable=False, ), 
                Field('review', 'text', label="What did you think of the product?", requires=IS_NOT_EMPTY()), 
                Field('score', 'double', default=0.00, label="Score (0.00 - 10.00)", requires=IS_FLOAT_IN_RANGE(0, 10, dot=".", error_message='Rating out of Range!')),
                Field('buy_again', 'boolean', label="Would you buy again?"),
                Field('date_posted', 'datetime', writable=False, default=get_current_time()),
)

db.Product_Table.id.readable = False
db.Product_Table.total_ratings.writable = db.Product_Table.total_possible_ratings.writable = False
auth.enable_record_versioning(db)