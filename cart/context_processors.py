from .cart import Cart

# create context processor

def cart(request):
    # return default data from cart
    # the cart is available in every page
    return{'cart':Cart(request)}
    