from store.models import Product

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



    def add(Self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        # logic
        if product_id in Self.cart:
            pass
        else:
            # Self.cart[product_id] = {'price': str(product.price)}
            Self.cart[product_id] = int(product_qty)

        Self.session.modified = True

    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        # get ids from cart
        product_ids = self.cart.keys()
        # use ids to lookup products in db model
        products = Product.objects.filter(id__in = product_ids)
        # return the lookeup products
        return products
    
    def get_quants(self):
        quantities= self.cart
        return quantities

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

		# Get cart
        ourcart = self.cart
		# Update Dictionary/cart
        ourcart[product_id] = product_qty
        self.session.modified = True
	

		# # Deal with logged in user
        # if self.request.user.is_authenticated:
		# 	# Get the current user profile
        #     current_user = Profile.objects.filter(user__id=self.request.user.id)
		# 	# Convert {'3':1, '2':4} to {"3":1, "2":4}
        #     carty = str(self.cart)
        #     carty = carty.replace("\'", "\"")
		# 	# Save carty to the Profile Model
        #     current_user.update(old_cart=str(carty))


        thing = self.cart
        return thing

