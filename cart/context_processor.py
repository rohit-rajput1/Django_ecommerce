from .cart import Cart

# Here are creating the context processor so our cart can work on all the pages of the website.
def cart(request):
    # Return the default data from our Cart.
    return {'cart': Cart(request)}