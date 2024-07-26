from django.shortcuts import render,redirect
from cart.cart import Cart
from payment.forms import ShippingForm,PaymentForm
from payment.models import ShippingAddress
from django.contrib import messages


from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import PaymentForm

from django.shortcuts import redirect
from django.contrib import messages

def process_order(request):
    if request.method == 'POST':
        # Get the billing information from the previous page
        payment_form = PaymentForm(request.POST or None)
        
        # Get shipping session data
        my_shipping = request.session.get('my_shipping')
        
        if my_shipping is None:
            messages.error(request, "Shipping information is missing.")
            return redirect('checkout')  # Redirect to a page to enter shipping details
        
        # Ensure all necessary keys are present
        required_keys = ['shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_state', 'shipping_zipcode', 'shipping_country']
        if not all(key in my_shipping for key in required_keys):
            messages.error(request, "Incomplete shipping information.")
            return redirect('checkout')  # Redirect to a page to enter shipping details

        # Create Shipping Address from session info
        shipping_address = (
            f"{my_shipping['shipping_address1']}\n"
            f"{my_shipping['shipping_address2']}\n"
            f"{my_shipping['shipping_city']}\n"
            f"{my_shipping['shipping_state']}\n"
            f"{my_shipping['shipping_zipcode']}\n"
            f"{my_shipping['shipping_country']}\n"
        )

        print(shipping_address)

        messages.success(request, "Order Placed!")
        return redirect('home')
    else:
        messages.error(request, "Access Denied!")
        return redirect('home')



def billing_info(request):
    if request.POST:
    # Get the Cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total() 

        # Create a session with Shipping Info
        my_shipping = request.POST
        request.session['shipping_info'] = my_shipping

        # check to see if user is logged in
        if request.user.is_authenticated:
            # Logged In
            billing_form = PaymentForm()
            return render(request, 'billing_info.html',{"cart_products":cart_products, "quantities":quantities, "totals":totals,"shipping_form":request.POST,'billing_form':billing_form})
        else:
            # Not Logged In
            billing_form = PaymentForm()
            return render(request, 'billing_info.html',{"cart_products":cart_products, "quantities":quantities, "totals":totals,"shipping_info":request.POST,'billing_form':billing_form})

        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'billing_info.html',{"cart_products":cart_products, "quantities":quantities, "totals":totals,"shipping_info":shipping_form})
    
    else:
        messages.success(request,"Access Denied!")
        return redirect('home')

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
        return render(request, 'checkout.html',)
    
