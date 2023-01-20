from django.shortcuts import render, redirect
from django.http import HttpResponseNotAllowed, HttpResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from index.models import About, Locations, Greeting
from index.forms import LocationsForm
from menu.models import Menu, Category
from news.models import News
from cart.models import Cart, CartMenu
from order.models import Order, OrderMenu, OrderPayment, OrderReceiver
from users.models import User, UserAddress
from contact.models import Contact, Subscribers
from users.forms import UserForm
from order.forms import OrderChangeStatusForm
from contact.forms import SubscribersForm
from django.db.models import Subquery, IntegerField, Count, OuterRef, CharField
from deluxe.decorators import superuser_required
from .filters import MenuFilter, NewsFilter, OrderFilter, UserFilter, ContactFilter, SubscribersFilter, CartFilter


# ---------------------------- WEBSITE -------------------------------------
@staff_member_required(login_url='/users/login/', redirect_field_name='next')
def index(request):
    context = {
        'title': "Dashboard",
        'page': 'home',
    }
    return render(request, 'dashboard.html', context)


@staff_member_required(login_url='/users/login/', redirect_field_name='next')
def menu(request):
    menu = Menu.objects.all().annotate(sold=Subquery(OrderMenu.objects.filter(menu=OuterRef('pk')).values(
        'menu').annotate(count=Count('id')).values('count'), output_field=IntegerField())).order_by('-created_at')
    filter = MenuFilter(request.GET, queryset=menu)
    menu = filter.qs

    context = {
        'title': 'Dashboard Menu',
        'menu': menu,
        'category': Category.objects.all(),
        'menufilter': filter,
        'page': 'menu'
    }
    return render(request, 'dashboard.html', context)


@staff_member_required(login_url='/users/login/', redirect_field_name='next')
def news(request):
    news = News.objects.all().order_by('-created_at')
    filter = NewsFilter(request.GET, queryset=news)
    news = filter.qs

    context = {
        'title': 'Dashboard News',
        'news': news,
        'page': 'news',
        'newsfilter': filter
    }
    return render(request, 'dashboard.html', context)


# ---------------------------- CART & ORDERS -------------------------------------
@staff_member_required(login_url='/users/login/', redirect_field_name='next')
def carts(request):
    carts = Cart.objects.annotate(menu_count=Subquery(CartMenu.objects.filter(cart=OuterRef(
        'pk')).values('cart').annotate(count=Count('id')).values('count'), output_field=IntegerField())).order_by('-created_at')

    filter = CartFilter(request.GET, queryset=carts)
    carts = filter.qs

    context = {
        'title': 'Dashboard Cart',
        'carts': carts,
        'cartfilter': filter,
        'page': 'carts',
    }
    return render(request, 'dashboard.html', context)


@staff_member_required(login_url='/users/login/', redirect_field_name='next')
def cartsdetail(request, token):
    cart = Cart.objects.filter(cart_token=token).get()
    cartmenu = CartMenu.objects.filter(cart__cart_token=token).all()
    context = {
        'title': 'Dashboard Cart Detail',
        'cart': cart,
        'cartmenu': cartmenu,
        'page': 'cartsdetail',
    }
    return render(request, 'dashboard.html', context)


@staff_member_required(login_url='/users/login/', redirect_field_name='next')
def orders(request):
    orders = Order.objects.annotate(payment_name=Subquery(OrderPayment.objects.filter(
        order=OuterRef('pk')).values('payment_method__name'), output_field=CharField())).order_by('-created_at')
    filter = OrderFilter(request.GET, queryset=orders)
    orders = filter.qs
    context = {
        'title': 'Dashboard Orders',
        'orders': orders,
        'page': 'orders',
        'ordersfilter': filter
    }
    return render(request, 'dashboard.html', context)


@staff_member_required(login_url='/users/login/', redirect_field_name='next')
def ordersdetail(request, token):
    order = Order.objects.filter(order_token=token).get()
    orderreceiver = OrderReceiver.objects.filter(
        order__order_token=token).get()
    orderpayment = OrderPayment.objects.filter(order__order_token=token).get()
    ordermenu = OrderMenu.objects.filter(order__order_token=token).all()
    context = {
        'title': 'Dashboard Order Detail',
        'order': order,
        'receiver': orderreceiver,
        'payment': orderpayment,
        'menu': ordermenu,
        'page': 'ordersdetail',
        'changestatusform': OrderChangeStatusForm(instance=order)
    }
    return render(request, 'dashboard.html', context)


# ---------------------------- USERS -------------------------------------
@staff_member_required(login_url='/users/login/', redirect_field_name='next')
def users(request):
    users = User.objects.all().order_by('-date_joined')
    filter = UserFilter(request.GET, queryset=users)
    users = filter.qs
    context = {
        'title': 'Dashboard Users',
        'users': users,
        'page': 'users',
        'usersfilter': filter
    }
    return render(request, 'dashboard.html', context)


@staff_member_required(login_url='/users/login/', redirect_field_name='next')
def userdetail(request, username):
    user = User.objects.filter(username=username).get()
    address = UserAddress.objects.filter(user__username=username).all()
    context = {
        'title': 'Dashboard User ' + username,
        'user': user,
        'address': address,
        'page': 'userdetail'
    }
    return render(request, 'dashboard.html', context)


@superuser_required
def edituser(request, username):
    if request.user.is_superuser:
        getuser = User.objects.filter(username=username).get()
        form = UserForm(instance=getuser)
        context = {
            'title': 'Dashboard Edit User | ' + username,
            'user': getuser.username,
            'form': form,
            'page': 'edituser'
        }
        return render(request, 'dashboard.html', context)
    else:
        return HttpResponseNotAllowed(permitted_methods=["GET"])


@superuser_required
def updateuser(request):
    if request.method == "POST":
        username = request.POST['user']
        user = User.objects.get(username=username)
        formset = UserForm(request.POST, instance=user)
        if formset.is_valid():
            formset.save()
            return redirect('/manager/users/'+username)
        else:
            context = {
                'title': 'Dashboard Edit User | ' + username,
                'user': username,
                'form': formset,
                'page': 'edituser'
            }
            return render(request, 'dashboard.html', context)
    else:
        return HttpResponseNotAllowed(['POST'])

# ---------------------------- CONTACTS -------------------------------------


@staff_member_required(login_url='/users/login/', redirect_field_name='next')
def contacts(request):
    contacts = Contact.objects.all()
    filter = ContactFilter(request.GET, queryset=contacts)
    contacts = filter.qs

    context = {
        'title': 'Dashboard Contacts',
        'contacts': contacts,
        'page': 'contacts',
        'contactsfilter': filter
    }
    return render(request, 'dashboard.html', context)


@staff_member_required(login_url='/users/login/', redirect_field_name='next')
def contactsdetail(request, id):
    contact = Contact.objects.filter(id=id).get()
    context = {
        'title': 'Dashboard Contacts Detail',
        'contact': contact,
        'page': 'contactdetail',
    }
    return render(request, 'dashboard.html', context)


@staff_member_required(login_url='/users/login/', redirect_field_name='next')
def subscribers(request):
    subscribers = Subscribers.objects.all().order_by('-created_at')
    filter = SubscribersFilter(request.GET, queryset=subscribers)
    subscribers = filter.qs
    context = {
        'title': 'Dashboard Subscribers',
        'subscribers': subscribers,
        'subscribersfilter': filter,
        'page': 'subscribers',
    }
    return render(request, 'dashboard.html', context)


@superuser_required
def subscribersedit(request, id):
    subscriber = Subscribers.objects.filter(id=id).get()
    formset = SubscribersForm(instance=subscriber)
    context = {
        'title': 'Dashboard Subscribers Edit',
        'subscriber': subscriber.email,
        'form': formset,
        'page': 'subscribersedit',
    }
    return render(request, 'dashboard.html', context)


# ---------------------------- OTHER -------------------------------------
@staff_member_required(login_url='/users/login/', redirect_field_name='next')
def about(request):
    if request.method == "POST":
        if request.user.is_superuser:
            text = request.POST['text']
            getabout = About.objects.get()
            getabout.text = text
            getabout.save()
            return redirect('/manager/about/')
        return HttpResponseNotAllowed()

    about = About.objects.get()
    context = {
        'title': 'Dashboard About',
        'about': about,
        'page': 'about'
    }
    return render(request, 'dashboard.html', context)


@staff_member_required(login_url='/users/login/', redirect_field_name='next')
def greeting(request):
    if request.method == "POST":
        text = request.POST['text']
        getgreeting = Greeting.objects.get()
        getgreeting.text = text
        getgreeting.save()
        return redirect('/manager/greeting/')

    greeting = Greeting.objects.get()
    context = {
        'title': 'Dashboard Greeting',
        'greeting': greeting,
        'page': 'greeting'
    }
    return render(request, 'dashboard.html', context)


@staff_member_required(login_url='/users/login/', redirect_field_name='next')
def locations(request):
    locations = Locations.objects.all()
    context = {
        'title': 'Dashboard Locations',
        'locations': locations,
        'page': 'locations'
    }
    return render(request, 'dashboard.html', context)


@staff_member_required(login_url='/users/login/', redirect_field_name='next')
def editlocation(request, city):
    location = Locations.objects.filter(city=city).get()
    form = LocationsForm(instance=location)
    context = {
        'title': 'Dashboard Edit Location',
        'location': location,
        'form': form,
        'page': 'editlocation'
    }
    return render(request, 'dashboard.html', context)


@staff_member_required(login_url='/users/login/', redirect_field_name='next')
def updatelocation(request):
    if request.method == "POST":
        getcity = Locations.objects.filter(city=request.POST['city']).get()
        getcity.address = request.POST['address']
        getcity.image = request.POST['image']
        getcity.save()
        return redirect('/manager/locations/')


@superuser_required
def addlocation(request):
    if request.method == "POST":
        formset = LocationsForm(request.POST)
        if formset.is_valid:
            formset.save()
        return redirect('/manager/locations/')
    context = {
        'title': 'Dashboard New Location',
        'page': 'addlocation',
        'form': LocationsForm
    }
    return render(request, 'dashboard.html', context)


def deletelocation(request):
    if request.user.is_superuser:
        if request.method == "POST":
            getloc = Locations.objects.filter(city=request.POST['city']).get()
            getloc.delete()
            return redirect('/manager/locations/')
    return HttpResponseNotAllowed()
