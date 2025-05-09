from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Dish, ShoppingCart, Order, Payment, User

# Register view
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful!")
            return redirect('login')
        else:
            messages.error(request, "Registration failed. Please check the information.")
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('dishes_list')  # Change 'home' to your landing page
            else:
                messages.error(request, "Invalid credentials.")
        else:
            messages.error(request, "Login failed. Please try again.")
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


@login_required
def dishes_list(request):
    dishes = Dish.objects.all()

    # Add dish to cart
    if request.method == 'POST':
        dish_id = request.POST.get('dish_id')
        dish = Dish.objects.get(id=dish_id)

        # Get or create the shopping cart for the logged-in user
        cart, created = ShoppingCart.objects.get_or_create(user=request.user)

        # Add the dish to the cart
        if dish not in cart.dishes.all():
            cart.dishes.add(dish)
            messages.success(request, f"{dish.name} added to your cart!")
        else:
            messages.info(request, f"{dish.name} is already in your cart!")

        return redirect('dishes_list')

    return render(request, 'core/dish_list.html', {'dishes': dishes})



@login_required
def cart_view(request):
    # Get or create the user's shopping cart
    cart, created = ShoppingCart.objects.get_or_create(user=request.user)

    # Remove dish from cart if requested
    if request.method == 'POST':
        dish_id = request.POST.get('remove_dish_id')
        if dish_id:
            dish = Dish.objects.get(id=dish_id)
            cart.dishes.remove(dish)
            messages.success(request, f"{dish.name} removed from your cart!")

    total_price = cart.total_price()
    dishes = cart.dishes.all()
    return render(request, 'core/cart.html', {'dishes': dishes, 'total_price': total_price})


@login_required
def checkout_view(request):
    # Get or create the user's shopping cart
    cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    dishes = cart.dishes.all()
    total_price = cart.total_price()

    # Check if the cart is empty
    if not dishes:
        messages.warning(request, "Your cart is empty. Add some dishes first!")
        return redirect('dishes_list')

    return render(request, 'core/checkout.html', {
        'dishes': dishes,
        'total_price': total_price,
    })

@login_required
def payment_view(request):
    # Get the user's shopping cart
    cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    dishes = cart.dishes.all()
    total_price = cart.total_price()

    if request.method == 'POST':
        # Create an order
        order = Order.objects.create(user=request.user, total=total_price)
        order.dishes.set(dishes)
        order.save()

        # Simulate payment
        Payment.objects.create(order=order, success=True)

        # Clear the cart after successful payment
        cart.dishes.clear()

        messages.success(request, "Payment successful! Your order has been placed.")
        return redirect('order_confirmation')

    return render(request, 'core/payment.html', {
        'total_price': total_price,
    })

@login_required
def order_confirmation(request):
    return render(request, 'core/order_confirmation.html')