from django.shortcuts import render, get_object_or_404 
# `get_object_or_404` is a shortcut function to get an object from the database or raise a 404 error if the object does not exist.
from .cart import Cart
from store.models import Product
from django.contrib import messages

# `JsonResponse` is like wrapping your data in a gift box. It takes your Python data and packages it nicely as JSON so it can be easily sent over the internet to a web browser or another program.
from django.http import JsonResponse

from django.http import HttpResponseBadRequest

# Create your views here.
def cart_summary(request):
    # Get the cart from cart.py
    cart = Cart(request)
    # Here we have store that fucntion in a variable called cart_products.
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, 'cart_summary.html',{"cart_products":cart_products, "quantities":quantities, "totals":totals})

def cart_add(request):
    # First we will get the cart from cart.py
    cart = Cart(request)
    # Test for POST request
    if request.POST.get('action') == 'post':
        # Get the Stuffs
        product_id = int(request.POST.get('product_id'))

        product_qty = int(request.POST.get('product_qty'))
        # Get the product from the database
        product = get_object_or_404(Product,id=product_id)
        
        # Save the session
        cart.add(product=product, quantity=product_qty)

        # Get Cart Quantity.
        cart_quantity = cart.__len__()

        # Return the response using JsonResponse
        # response = JsonResponse({'Product Name: ': product.name})
        response = JsonResponse({'qty:': cart_quantity})
        messages.success(request, "Item has been added to the cart.") 
        return response




def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Delete Stuffs
        product_id = int(request.POST.get('product_id'))

    # Now we will call the delete function in the Cart.
    cart.delete(product=product_id)

    response = JsonResponse({'product': product_id})
    messages.success(request, "Item has been deleted from the cart.") 
    return response




def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get Stuffs
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id,quantity=product_qty)
        response = JsonResponse({'qty': product_qty})
        messages.success(request, "Cart has been updated.") 
        return response