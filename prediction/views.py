from django.shortcuts import render,redirect,get_object_or_404

from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import UserProfile,Dress
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .models import Category, Dress,Cart,Order
from django.contrib.auth.decorators import login_required



# Create your views here.
def index(request):
    products = Dress.objects.all()
    return render(request, 'index.html', {'products': products})

def contact(request):
    return render(request, 'contact.html')


def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        age = request.POST['age']
        place = request.POST['place']
        contact_number = request.POST['contact_number']
        image = request.FILES.get('user_image')
        gender = request.POST['gender']

        errors = {}

        if User.objects.filter(username=username).exists():
            errors['username'] = "Username already exists!"

        try:
            validate_email(email)
        except ValidationError:
            errors['email'] = "Invalid email format!"

        if User.objects.filter(email=email).exists():
            errors['email'] = "Email already exists!"

        if UserProfile.objects.filter(contact_number=contact_number).exists():
            errors['contact_number'] = "This contact number is already registered!"

        if password != confirm_password:
            errors['password'] = "Passwords do not match!"

        if errors:
            return render(request, 'register.html', {'errors': errors})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = True
        user.save()

        UserProfile.objects.create(
            user=user,
            age=age,
            place=place,
            contact_number=contact_number,
            image=image,
            gender=gender
        )

        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login')

    return render(request, 'register.html')



def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            if not user.is_active:
                messages.error(request, "Your account is pending approval by the admin.")
                return redirect('login')

            login(request, user)

            if user.is_superuser:  
                return redirect("admin_panel:admin_dashboard")  
            
            elif UserProfile.objects.filter(user=user).exists():
                messages.success(request, "Login successful! Welcome to your profile.")
                return redirect("home")
            
            else:
                messages.success(request, "Login successful!")
                return redirect("home_page")  

        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')

def home(request):
    categories = Category.objects.all()
    dresses = Dress.objects.all()
    return render(request, 'home.html', {'categories': categories, 'dresses': dresses})

def dresses_by_category(request, category_id):
    category = Category.objects.get(id=category_id)
    dresses = Dress.objects.filter(category=category)
    return render(request, 'dresses_by_category.html', {'category': category, 'dresses': dresses})

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Dress, pk=pk)
    return render(request, 'details.html', {'product': product})



@login_required
def add_to_cart(request, product_id):
    product = Dress.objects.get(id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('view_cart')  # Redirect to cart page

@login_required
def view_cart(request):
    cart_items = Order.objects.filter(user=request.user, status='Pending')
    
    total = 0
    for item in cart_items:
        item.total_price = item.product.price * item.quantity
        total += item.total_price  # Sum total price for all items

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Dress, id=product_id)
    if request.method == "POST":
        order = Order.objects.create(user=request.user, product=product, quantity=1)
        return redirect('order_confirmation', order_id=order.id)
    return render(request, 'buy_now_confirm.html', {'product': product})


@login_required
def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id)
    total_price = order.product.price * order.quantity
    return render(request, 'order_confirmation.html', {'order': order, 'total_price': total_price})


def confirm_purchase(request):
    if request.method == 'POST':
        cart_items = Order.objects.filter(user=request.user, status='Pending')
        for item in cart_items:
            item.status = 'Ordered'
            item.save()
        return redirect('home')  # After confirming, go to homepage
 
