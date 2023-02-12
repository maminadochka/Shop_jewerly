from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as DjangoUser
from .forms import LoginForm, UserForm
from django.contrib.auth import logout, login
from django.contrib.auth import authenticate
from .models import Category, Product
from cart.forms import CartForm


# Create your views here.


def main_page(request):
    return render(request, 'main/main_page.html')


def logout_page(request):
    logout(request)
    return redirect('home')


def login_page(request):
    error = ''
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return redirect('login')
        else:
            error = 'ERROR!'
    else:
        form = LoginForm()
    return render(request, 'main/login_page.html', {
        'form': form,
        'error': error,
    })


def sign_up(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserForm()
    return render(request, 'main/sign_up.html', {'form': form})


@login_required()
def profile(request):
    user = request.user
    if user.is_authenticated:
        user_name = user
        email = request.user.email
    return render(request, 'main/profile.html',
                  {'user_name': user_name, 'email': email, })


def catalog_page(request, category_slug=None): #products list
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'main/catalog.html',
                 {'category': category,
                  'categories': categories,
                  'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartForm()
    return render(request, 'main/product_detail.html',
                  {'product': product, 'cart_product_form': cart_product_form})

