from django.shortcuts import render, redirect
from django.http import HttpResponse, QueryDict
from django.db.models import Q
from deluxe import settings
from order.models import Payment, Order, OrderMenu, OrderPayment, OrderReceiver, Status
from order.forms import OrderChangeStatusForm
from menu.models import Menu, Rate
from cart.models import Cart, CartMenu
from django.db.models import Subquery, OuterRef, Model, DecimalField, IntegerField, TextField, URLField, Count
from users.models import User
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseForbidden
from deluxe.decorators import ordermanager_required
from manager.filters import OrderManagerFilter
import random
import string
import xendit
from xendit import EWallet, RetailOutlet
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def orders(request):
    status = request.GET['status']

    getstatus = Status.objects.filter(status=status).get()
    component = 0
    getmenu = {}

    getorder = Order.objects.filter(user__username=request.user.username, status__status=getstatus.status).annotate(
        menu_image=Subquery(OrderMenu.objects.filter(order=OuterRef('pk')).values('menu__image')[:1], output_field=URLField())).annotate(menucount=Subquery(OrderMenu.objects.filter(order=OuterRef('pk')).values('order').annotate(count=Count('id')).values('count'), output_field=IntegerField())).order_by('-update_at')

    if getstatus.code == 101:
        component = 0
        getmenu = OrderMenu.objects.filter(
            order__user__username=request.user.username, order__status__status=getstatus.status).all()

    if getstatus.code != 101:
        component = 1

    context = {
        'title': getstatus.text,
        'orders': getorder,
        'menu': getmenu,
        'component': component
    }

    return render(request, 'order.html', context)


@login_required
def order(request, token):
    if Order.objects.filter(order_token=token, user__username=request.user.username).exists() or request.user.groups.filter(name="OrderManager").exists():
        getorder = Order.objects.filter(order_token=token).get()
        getreceiver = OrderReceiver.objects.filter(
            order__order_token=token).get()
        getpayment = OrderPayment.objects.filter(
            order__order_token=token).get()
        getmenu = OrderMenu.objects.filter(order__order_token=token).all().annotate(userrate=Subquery(Rate.objects.filter(
            menu=OuterRef('menu'), user__username=request.user.username).values('rating'), output_field=IntegerField()))

        totalmenu = 0

        for m in getmenu:
            totalmenu += m.total

        context = {
            'title': 'Detail Order',
            'order': getorder,
            'receiver': getreceiver,
            'payment': getpayment,
            'menu': getmenu,
            'totalmenu': totalmenu
        }

        return render(request, 'order-detail.html', context)
    return HttpResponseForbidden()


def get_random_string(length):
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters)
                         for i in range(length))
    # print random string
    return result_str


@login_required
def create(request):
    if request.method == "POST":
        x = xendit.Xendit(
            api_key=settings.XENDIT_API_KEY)

        name = request.POST['name']
        phone_number = request.POST['phone_number']
        address = request.POST['address']
        city = request.POST['city']
        payment = request.POST['payment']
        total = request.POST['alltotal']

        getcart = Cart.objects.filter(
            user__username=request.user.username).get()
        getcartmenu = CartMenu.objects.filter(
            cart__user__username=request.user.username).all()
        getuser = User.objects.filter(username=request.user.username).get()
        getpayment = Payment.objects.filter(slug=payment).get()
        getstatus = Status.objects.filter(status="notpaid").get()
        getstatus2 = Status.objects.filter(status="onprocess").get()

        order_token = 'DLX-'+get_random_string(20)
        order = Order(order_token=order_token, user=getuser,
                      status=getstatus, total=total)
        order.save()

        getorder = Order.objects.filter(order_token=order_token).get()
        orderreceiver = OrderReceiver(
            order=getorder, name=name, phone_number=phone_number, address=address, city=city)

        payment_code = ""
        direct = ""

        if getpayment.type == "retail-outlet":
            createpaymentcode = x.RetailOutlet.create_fixed_payment_code(
                external_id="deluxe_fix_payment_code",
                retail_outlet_name=getpayment.channel_code,
                name=request.user.username,
                expected_amount=total,
            )
            payment_code = createpaymentcode.payment_code
            direct = "/order/pay/"

        if getpayment.type == "cod":
            payment_code = "DLX-COD -" + get_random_string(10)
            order.status = getstatus2
            order.save()
            direct = "/order?status=onprocess"

        orderpayment = OrderPayment(
            order=getorder, payment_method=getpayment, payment_token=payment_code)
        orderreceiver.save()
        orderpayment.save()

        for m in getcartmenu:
            ordermenu = OrderMenu(
                order=getorder, menu=m.menu, quantity=m.quantity, total=m.total)
            ordermenu.save()

        getcart.delete()
        getcartmenu.delete()
        return redirect(direct)
    return HttpResponseNotFound(render(request, 'pages/404.html'))


@login_required
def pay(request):
    if request.method == "POST":
        order = request.POST['order']
        getstatus = Status.objects.filter(status="onprocess").get()
        getorder = Order.objects.filter(order_token=order).get()
        getorder.status = getstatus
        getorder.save()

        return redirect('/order?status=onprocess')

    if Order.objects.filter(user__username=request.user.username, status__status="notpaid").exists():
        order = Order.objects.filter(
            user__username=request.user.username, status__status="notpaid").get()
        orderpayment = OrderPayment.objects.filter(
            order__user__username=request.user.username, order__status__status="notpaid").get()
        payment = Payment.objects.filter(
            slug=orderpayment.payment_method.slug).get()
        context = {
            'title': 'Pay',
            'order': order,
            'payment': orderpayment,
            'name': payment
        }

        return render(request, 'pay.html', context)
    else:
        return redirect('/users/')


@login_required
def payment(request):
    slug = request.GET['slug']
    getpayment = Payment.objects.filter(slug=slug).get()
    return JsonResponse({
        'confirm': '200',
        'fee': getpayment.fee
    })


@login_required
def changestatus(request):
    if request.method == "POST":
        token = request.POST['token']
        if Order.objects.filter(order_token=token, user__username=request.user.username).exists() or request.user.groups.filter(name="OrderManager").exists():
            
            getstatus = request.POST['status']
            order = Order.objects.get(order_token=token)
            status = Status.objects.get(status=getstatus)
            order.status = status
            order.save()

            return redirect(request.POST['next'])
        
        return HttpResponseForbidden()
    return HttpResponseNotFound(render(request, 'pages/404.html'))


@login_required
def orderreceived(request):
    if request.method == "POST":
        order = Order.objects.filter(
            user__username=request.user.username, status__status="received").get()
        status = Status.objects.filter(status="finished").get()
        order.status = status
        order.save()

        return redirect('/order/?status=finished')
    return HttpResponseNotFound(render(request, 'pages/404.html'))


@login_required
def ordercancel(request):
    if request.method == "POST":
        token = request.POST['token']
        order = Order.objects.filter(order_token=token).get()
        status = Status.objects.filter(status="canceled").get()
        order.status = status
        order.save()
        return redirect('/order/?status=canceled')
    return HttpResponseNotFound(render(request, 'pages/404.html'))


# MANAGER
@ordermanager_required
def ordermanager(request):
    waiting = Order.objects.filter(status__status="onprocess").all()
    onprocess = Order.objects.filter(Q(status__code=101) | Q(
        status__code=202)).all().order_by('-update_at')
    newest = Order.objects.all().order_by('-update_at')[:10]
    finished = Order.objects.filter(
        status__status="finished").all().order_by('-update_at')[:10]

    context = {
        'title': "Main Orders",
        'waiting': waiting,
        'onprocess': onprocess,
        'newest': newest,
        'finished': finished,
        'changestatusform': OrderChangeStatusForm,
        'context': "main"
    }

    return render(request, 'order-manager.html', context)


@ordermanager_required
def ordermanagerall(request):
    orders = Order.objects.all().order_by('-created_at')
    filter = OrderManagerFilter(request.GET, queryset=orders)
    orders = filter.qs
    context = {
        'title': "All Orders",
        'orders': orders,
        'ordersfilter': filter,
        'context': "all"
    }
    return render(request, 'order-manager.html', context)
