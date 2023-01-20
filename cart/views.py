from django.core import serializers
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from menu.models import Menu
from users.models import User, UserAddress
from index.models import Locations
from cart.models import Cart, CartMenu
from order.models import Payment, Delivery, Order
from django.contrib.auth.decorators import login_required
import random
import string
from decimal import Decimal
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def count(request):
    if request.user.is_authenticated:
        cartcount = CartMenu.objects.filter(
            cart__user__username=request.user.username).count()

    else:
        cartcount = 0

    return JsonResponse({
        'count': cartcount
    })


def index(request):

    checkout = True
    checkoutstatus = ""
    if Order.objects.filter(user__username=request.user.username, status__code=101).exists():
        checkout = False
        checkoutstatus = Order.objects.filter(
            user__username=request.user.username, status__code=101).get().status

    cartexists = CartMenu.objects.filter(
        cart__user__username=request.user.username).exists()

    cartmenu = CartMenu.objects.filter(
        cart__user__username=request.user.username).all()
    cartcount = CartMenu.objects.filter(
        cart__user__username=request.user.username).count()
    context = {
        'title': 'Cart',
        'cartexists': cartexists,
        'cartmenu': cartmenu,
        'cartcount': cartcount,
        'checkout': checkout,
        'checkoutstatus': checkoutstatus
    }

    return render(request, 'cart.html', context)


@login_required(redirect_field_name='/cart/')
def checkout(request):

    if Order.objects.filter(user__username=request.user.username, status__code=101).exists():
        checkoutstatus = Order.objects.filter(
            user__username=request.user.username, status__code=101).get().status
        messages.info(
            request, f"You have order on {checkoutstatus} please wait until that finished")
        return redirect('/cart/')

    address = {}
    if UserAddress.objects.filter(user__username=request.user.username, default=True).exists():
        address = UserAddress.objects.filter(
            user__username=request.user.username, default=True).get()
    elif UserAddress.objects.filter(user__username=request.user.username).exists():
        address = UserAddress.objects.filter(
            user__username=request.user.username).latest("created_at")

    if Cart.objects.filter(user__username=request.user.username).exists():
        menu = CartMenu.objects.filter(
            cart__user__username=request.user.username).all()
        context = {
            'title': 'Checkout',
            'totalmenu': Cart.objects.filter(user__username=request.user.username).get(),
            'menu': menu,
            'city': Locations.objects.all().values('city'),
            'payment': Payment.objects.values(),
            'delivery': Delivery.objects.get(),
            'address': address
        }
        return render(request, 'checkout.html', context)
    else:
        return redirect('/cart/')


def get_random_string(length):
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters)
                         for i in range(length))
    # print random string
    return result_str

# CRUD


def updatealltotal(username):
    totalall = 0
    getallmenu = CartMenu.objects.filter(
        cart__user__username=username).all()
    for a in getallmenu:
        totalall += a.total
    getallcart = Cart.objects.filter(
        user__username=username).get()
    getallcart.total = totalall
    getallcart.save()


@login_required
def add(request):
    slug = request.POST['slug']
    getuser = User.objects.filter(username=request.user.username).get()
    getmenu = Menu.objects.filter(slug=slug).get()

    if Cart.objects.filter(user__username=request.user.username).exists():

        if CartMenu.objects.filter(cart__user_id=request.user.id).exists() and CartMenu.objects.filter(menu_id=getmenu.id).exists():
            getcartmenu = CartMenu.objects.filter(
                cart__user_id=request.user.id) and CartMenu.objects.filter(menu_id=getmenu.id).get()
            getcartmenu.quantity = getcartmenu.quantity + 1
            getcartmenu.total = getcartmenu.total + getmenu.price
            getcartmenu.save()

        else:
            getcart = Cart.objects.filter(
                user__username=request.user.username).get()
            cartmenu = CartMenu(cart=getcart, menu=getmenu, quantity=1)
            cartmenu.total = cartmenu.total + getmenu.price
            cartmenu.save()

    else:
        token = 'DLX-CART-'+get_random_string(10)

        cart = Cart(cart_token=token, user=getuser)
        cart.save()

        getcart = Cart.objects.filter(cart_token=token).get()
        cartmenu = CartMenu(cart=getcart, menu=getmenu, quantity=1)
        cartmenu.total = cartmenu.total + getmenu.price
        cartmenu.save()

    updatealltotal(request.user.username)

    return JsonResponse({
        'confirm': '200',
    })


@login_required
# @csrf_exempt
def quantity(request):
    slug = request.POST['slug']
    qty = request.POST['qty']
    getmenu = Menu.objects.filter(slug=slug).get()
    getcartmenu = CartMenu.objects.filter(
        menu__slug=slug).get()
    getcartmenu.quantity = qty
    getcartmenu.total = getmenu.price * Decimal(qty)
    getcartmenu.save()

    updatealltotal(request.user.username)

    return JsonResponse({
        'confirm': '200'
    })


@login_required
def delete(request):
    if request.method == "POST":
        cartmenu = CartMenu.objects.filter(
            menu__slug=request.POST['slug']).get()
        cartmenu.delete()
        updatealltotal(request.user.username)

    countmenu = CartMenu.objects.filter(
        cart__user__username=request.user.username).count()
    if countmenu < 1:
        cart = Cart.objects.filter(user__username=request.user.username).get()
        cart.delete()

    return JsonResponse({
        'confirm': '200',
        'count': countmenu
    })


@login_required
def deleteall(request):
    if request.method == "POST":
        if request.user.is_superuser or request.user.is_staff:

            token = request.POST['cart_token']
            cart = Cart.objects.get(cart_token=token)
            cart.delete()

            return redirect('/manager/carts/')
        else:
            cart = Cart.objects.filter(
                user__username=request.user.username).get()
            cart.delete()
            return redirect('/cart')
    return HttpResponseNotFound(render(request, 'pages/404.html'))
