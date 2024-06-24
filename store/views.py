from django.shortcuts import render,redirect
from .models import Product, Category ,Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Now we will import the User model to create user by using "from django.contrib.auth.models"
from django.contrib.auth.models import User
# Now we will import UserCreationForm to create form for user registration.
from django.contrib.auth.forms import UserCreationForm
# Now we will import SignUpForm from form.py file.
from .form import SignUpForm,UpdateUserForm,ChangePasswordForm,UserInfoForm
from django import forms
from django.db.models import Q
import json
from cart.cart import Cart

def search(request):
    if request.method == 'POST':
        searched =request.POST['searched']
        # Here we will query the database model and it will be case insensitive.
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        if not searched:
            messages.success(request, "This Product is not there!!!")
            return render(request,'search.html',{'searched':searched})
        else:
            return render(request,'search.html',{'searched':searched})
    else:
        return render(request,'search.html',{})

def update_info(request):
    # if request.user.is_authenticated:
    #     current_user =Profile.objects.get(id=request.user.id)
    #     form = UserInfoForm(request.POST or None, instance=current_user)

    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, "Your Info has been updated.")
    #         return redirect('home')
    #     return render(request, "update_info.html",{'form':form})
	# # return render(request, 'update_user.html', {})
    # else:
    #     messages.success(request, "You must be logged in to view this page.")
    #     return redirect('home')
    #     #return render(request, 'update_info.html', {})
    if request.user.is_authenticated:
        try:
            current_user = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            current_user = Profile(user=request.user)
            current_user.save()

        form = UserInfoForm(request.POST or None, instance=current_user)

        if form.is_valid():
            form.save()
            messages.success(request, "Your info has been updated.")
            return redirect('home')

        return render(request, "update_info.html", {'form': form})
    else:
        messages.error(request, "You must be logged in to view this page.")
        return redirect('home')

def update_password(request):   
    if request.user.is_authenticated:
        current_user = request.user
        # Did they fill out the form?
        if request.method == 'POST':
            form = ChangePasswordForm(current_user,request.POST)
            # Did the form validate?
            if form.is_valid():
                form.save()
                messages.success(request, "Password has been updated.")
                login(request,current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})   
    else:
        messages.success(request, "You must be logged in to view this page.")
        return redirect('home')


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, "User has been updated.")
            return redirect('home')
        return render(request, "update_user.html",{'user_form':user_form})
	# return render(request, 'update_user.html', {})
    else:
        messages.success(request, "You must be logged in to view this page.")
        return redirect('login')


def category_summary(request):
    categories = Category.objects.all()
    return render(request,'category_summary.html',{"categories":categories})


# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request,'home.html',{'products':products})


def about(request):
    return render(request,'about.html',{})

def login_user(request):
    if request.method == "POST":
        # Using .get() instead of indexing to avoid KeyError
        username = request.POST.get('username')
        password = request.POST.get('password')

        # If either username or password is not provided, handle the error
        if not username or not password:
            messages.error(request, "Please provide both username and password.")
            return redirect('login')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # On login Get User Profile
            current_user = Profile.objects.get(user__id=request.user.id)
            # Now we want to get their saved cart from the database.
            saved_cart = current_user.old_cart
            # Now we will convert the database string to a list.
            if saved_cart:
                # Convert to dictionary using JSON
                converted_cart = json.loads(saved_cart)

                # Now we want to add the loaded dictionary to our sessions
                cart = Cart(request)

                # Here we will loop through the cart and add the items from the database in a key, value pair because of python dictionary.
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, "You are now logged in.")
            return redirect('home')
        else:
            messages.error(request, "Error Occurred! Please try again.")
            return redirect('login')
    else:
        # If people didn't fill out the form they just want to see the webpage.
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "You are now logged out.")
    # so after logout user (request) will be redirected to home page.
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():  # Corrected spelling of is_valid()
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # login user after registration
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "Kudos Username Created - Please fill out you User Info...")  # Removed unnecessary parentheses
            return redirect('update_info')
        else:
            messages.success(request, "Error Occurred! Please try again.")  # Fixed typo in message
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})  # Corrected dictionary key-value pair

def product(request,pk):
    # So this will us into product model and get the product with the primary key of pk.
    product= Product.objects.get(id=pk)
    return render(request,'product.html',{'product':product})

def category(request,foo):
    # So this foo is the category name which we will get from the url.
    foo = foo.replace('-',' ') # So this will replace the '-' with ' ' in the category name.

    # Grab the category name from the url and get the products with that category name.
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request,'category.html',{'category':category,'products':products})
    except:
        messages.success(request, "Category does not exist.")
        return redirect('home')