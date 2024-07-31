from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from .models import Category
from django.db.models import Q
import json
from cart.cart import Cart

def search(request):
    # know if they have filled the form 
    if request.method == "POST":
        searched = request.POST['searched']
        # query db models
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        # test for null
        if not searched:
             messages.error(request, "That Product Does Not Exists.")
             return render(request, 'search.html', {})
        else:
            return render (request, "search.html", {'searched':searched})
    else:   
        return render (request, "search.html", {})


def update_info(request):
    if request.user.is_authenticated:
        try:
            current_user = Profile.objects.get(user__id = request.user.id)
        except Profile.DoesNotExist:
            messages.error(request, "Profile does not exist. Please create your profile first.")
            return redirect('home')  # Adjust this to the appropriate URL or view where the user can create a profile
        
        form =UserInfoForm (request.POST or None, instance = current_user)

        if form.is_valid():
            form.save()
            messages.success(request, "Your Info has been Updated")
            return redirect('home')
        return render(request, 'update_info.html', {'form':form})
    else:
        messages.success(request, "You must be logged in to access that page!")
        return redirect('home')
  
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # did they fill the form
        if request.method == 'POST':
            form = ChangePasswordForm (current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your Password has been updated...")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')

        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {'form':form})
    else:
        messages.success(request, "You must be logged in to view the page")
        return redirect('home')

def update_user(request):

    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form =UpdateUserForm (request.POST or None, instance = current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User has been Updated.")
            return redirect ('home')

        return render(request, 'update_user.html', {'user_form':user_form})
    else:
        messages.success(request, "You must be logged in to access that page!")
        return redirect('home')
         

def category_summary(request):
    categories = Category.objects.all()

    return render(request, 'category_summary.html', {'categories': categories})
    
def category(request, foo):
    foo = foo.replace('-', '') #replaces hypen with space
    # grab the category from the url
    try:
        # lookup the category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category': category})
    except:
        messages.success(request, ("that category doesnt exists"))
        return redirect(request, 'home')
         


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
    
    return render(request, 'About.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # shopping cart
            current_user = Profile.objects.get(user__id=request.user.id)
            # get their saved cart from db
            saved_cart = current_user.old_cart
            # convert db string to python dict
            if saved_cart:
                # convert to dict using json
                converted_cart = json.loads(saved_cart)
                # add the loaded dict to our session
                cart = Cart(request)
                # loop through the cart and add items from db
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, ('You have been logged in'))
            return redirect('home')
        else:
            messages.success(request, ('There was an error, please try again'))
            return redirect('login')
    else:
        
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out"))
    return redirect('home')


def register_user(request):
    form = SignUpForm ()
    if request.method == "POST":
        form =  SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Username Created - Please Fill OUt Your User Info!"))
            return redirect('update_info')
        else:
            messages.success(request, ("There was a problem!"))
            return redirect('register')
    else:

        return render(request, 'register.html', {'form':form})
