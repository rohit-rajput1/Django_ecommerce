from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session

        #Get Request
        self.request = request

        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # Ensure the cart is available on all the pages of the website.
        if 'session_key' not in self.session:
            # If the session key doesn't exist, initialize an empty cart and store it in the session and assign the empty cart to the cart variable.
            cart = self.session['session_key'] = {}
        
        # Now, assign the cart to the instance's attribute
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        # Logic to check if the product is already in the cart.
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price), 'qty': product_qty}
            # we have passed the integer of the product quantity.
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        if self.request.user.is_authenticated:
            #Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #Convert the cart to a string "{'1': 2, '2': 3} to {"1":2,"2":3}"
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # Now we will the carty variable in to the profile model.
            current_user.update(old_cart=str(carty))

    def cart_total(self):
        # get product ids from the cart
        product_ids = self.cart.keys()

        # Now we want to lookup those keys in our product database.
        products = Product.objects.filter(id__in=product_ids)

        # Now we want to get quantities
        quantities = self.cart

        # so we initailize a total variable and count start from 0.
        total = 0

        # Now we want to loop through the products and get the total price of the products.

        for key,value in quantities.items():
            # now we will convert the key to an integer for math
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)                    
        return total




    def __len__(self):
        # So this method will return the number of items in the cart.
        return len(self.cart)
    
    def get_prods(self):
        # get ids from the cart
        product_ids =  self.cart.keys()
        # use the ids to look up products in database model.
        products = Product.objects.filter(id__in=product_ids)

        # returned those looked up products
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        # Getting the cart
        ourcart = self.cart

        # Updating the cart
        ourcart[product_id] = product_qty


        self.session.modified = True

        thing =self.cart
        return thing
    
    def delete(self,product):
        product_id = str(product)
        # Delete from dictionary/cart 
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True