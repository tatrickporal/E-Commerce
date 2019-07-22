MY_STRINGS = db(db.Product).select()

@auth.requires_signature(hash_vars=False)
def search():
    s = request.vars.search_string or ''
    res = [t for t in MY_STRINGS if s in t.product_name]
    return response.json(dict(strings=res))