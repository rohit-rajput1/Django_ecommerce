from django.shortcuts import render
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress

def payment_success(request):
    return render(request, 'payment_success.html')

def checkout(request):
    # Get the Cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        # Checkout as the loggedIn user
        shipping_user = ShippingAddress.objects.get(user=request.user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'checkout.html',{"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})
    else:
        # This is preferable when someone visited the website as guest.
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'checkout.html',{"cart_products":cart_products, "quantities":quantities, "totals":totals,"shipping_form":shipping_form})