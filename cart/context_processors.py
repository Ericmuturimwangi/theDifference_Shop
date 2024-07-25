from .cart import Cart

# create context processor

def cart(request):
    # return default data from cart
    return{'cart':Cart(request)}
    