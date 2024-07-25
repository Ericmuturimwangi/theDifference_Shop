class Cart():
    def __init__(Self, request):
        Self.session = request.session

        # get session key if it exists

        cart = Self.session.get('session_key')
        # if user is new, no session key
        if 'session_key' not in request.session:
            cart = Self.session['session_key'] = {} 

        # make sure the cart is available on all pages

        Self.cart = cart

