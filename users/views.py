from deluxe import settings
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from deluxe.decorators import costumer_required
from django.contrib.auth import authenticate, login as login_process, logout as logout_process, update_session_auth_hash
from django.contrib import messages
from .models import User, UserToken, UserAddress
from order.models import Order
from django.contrib.auth.models import Group
from django import forms
from index.models import Locations
import random
from datetime import datetime, timedelta, timezone
from dateutil import parser
import string
from .forms import LoginForm, RegisterForm, ChangePasswordForm, ForgotPasswordForm, ResetPasswordForm, DeleteUserForm
from deluxe.decorators import superuser_required


@login_required(login_url='/users/login', redirect_field_name='next')
def index(request):
    anyorder = False
    if Order.objects.filter(user__username=request.user.username, status__code=101).exists():
        anyorder = Order.objects.filter(
            user__username=request.user.username, status__code=101).get()
    context = {
        'title': request.user.username,
        'anyorder': anyorder,
    }
    return render(request, 'users.html', context)


@login_required
def account(request):
    context = {
        'title': 'Account',
        'page': "account"
    }

    return render(request, 'account-settings.html', context)


@login_required
def address(request):
    addresscount = UserAddress.objects.filter(
        user__username=request.user.username).count()
    context = {
        'title': 'Address',
        'address': UserAddress.objects.filter(user__username=request.user.username).all().order_by('-default'),
        'page': "address",
        'addresscount': addresscount
    }
    return render(request, 'account-settings.html', context)


def get_random_string(length):
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters)
                         for i in range(length))
    # print random string
    return result_str


@login_required
def newaddress(request):
    if request.method == "POST":

        getuser = User.objects.filter(username=request.user.username).get()
        street = request.POST['street']
        city = request.POST['city']
        zip_code = request.POST['zip_code']
        default = False

        if not UserAddress.objects.filter(user__username=request.user.username).exists():
            default = True

        if 'default' in request.POST:
            if UserAddress.objects.filter(user__username=request.user.username, default=True).exists():
                getdef = UserAddress.objects.filter(
                    user__username=request.user.username, default=True).all()
                for d in getdef:
                    d.default = False
                    d.save()
            default = True

        address_code = "DLX-ADRSS-" + get_random_string(15)

        newaddress = UserAddress(
            user=getuser, address_code=address_code, street=street, city=city, zip_code=zip_code, default=default)
        newaddress.save()
        return redirect('/users/settings/address/')

    if UserAddress.objects.filter(user__username=request.user.username).count() == 3:
        return redirect('/users/address/')
    locations = Locations.objects.all()
    context = {
        'title': 'New Address',
        'locations': locations,
        'page': 'newaddress'
    }
    return render(request, 'account-settings.html', context)


@login_required
def editaddress(request, code):

    getaddress = UserAddress.objects.filter(address_code=code).get()
    locations = Locations.objects.all()
    context = {
        'title': 'New Address',
        'address': getaddress,
        'locations': locations,
        'page': 'editaddress'
    }
    return render(request, 'account-settings.html', context)


@login_required
def updateaddress(request):
    if request.method == "POST":
        code = request.POST['code']
        street = request.POST['street']
        city = request.POST['city']
        zip_code = request.POST['zip_code']
        default = False

        if 'default' in request.POST:
            if UserAddress.objects.filter(user__username=request.user.username, default=True).exists():
                getdef = UserAddress.objects.filter(
                    user__username=request.user.username, default=True).all()
                for d in getdef:
                    d.default = False
                    d.save()

            default = True

        getaddress = UserAddress.objects.filter(address_code=code).get()
        getaddress.street = street
        getaddress.city = city
        getaddress.zip_code = zip_code
        getaddress.default = default
        getaddress.save()

        return redirect('/users/settings/address/')
    return HttpResponseNotFound(render(request, 'pages/404.html'))


@login_required
def deleteaddress(request):
    if request.method == "POST":
        code = request.POST['code']
        getaddress = UserAddress.objects.filter(address_code=code).get()

        if getaddress.default == True:
            getcountaddress = UserAddress.objects.filter(
                user__username=request.user.username).count()

            if getcountaddress > 1:
                getanotheraddress = UserAddress.objects.filter(
                    user__username=request.user.username).first()
                getanotheraddress.default = True
                getanotheraddress.save()

        getaddress.delete()

        return redirect('/users/settings/address/')
    return HttpResponseNotFound(render(request, 'pages/404.html'))

# AUTH


def login(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        form = LoginForm(request.POST)

        theme = False
        if 'is_dark' in request.session:
            theme = request.session['is_dark']

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login_process(request, user)

                if theme == True:
                    request.session['is_dark'] = True

                if 'next' in request.POST:
                    return redirect(request.POST['next'])
                else:
                    return redirect('/')
            else:
                messages.error(request,
                               "Your data is not match io our credential, please check again")
                return render(request, 'auth/login.html', {'title': 'Login', 'form': form})

    else:
        form = LoginForm

    return render(request, 'auth/login.html', {'title': 'Login', 'form': form})


@login_required
def logout(request):
    if request.method == "POST":

        theme = False
        if 'is_dark' in request.session:
            theme = request.session['is_dark']

        logout_process(request)

        if theme == True:
            request.session['is_dark'] = True
        if request.POST['next'] == "/users/" or request.POST['next'] == '/manager/' or request.POST['next'] == '/order/':
            return redirect(settings.LOGOUT_REDIRECT_URL)
        else:
            return redirect(request.POST['next'])

    return HttpResponseNotFound(render(request, 'pages/404.html'))


def register(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():
            costumergroup = Group.objects.get(name="Costumer")

            fullname = request.POST['fullname']
            username = request.POST['username']
            email = request.POST['email']
            phone_number = request.POST['phone_number']
            password1 = request.POST['password1']
            register = User.objects.create_use(
                fullname=fullname, username=username, email=email, phone_number=phone_number, password=password1)


            if register:
                User.objects.get(username=username).groups.add(costumergroup)
                user = authenticate(
                    request, username=username, password=password1)
                login_process(request, user)
                return redirect('/')

        return render(request, 'auth/register.html', {'title': 'Register', 'form': form})

    else:
        form = RegisterForm
    return render(request, 'auth/register.html', {'title': 'Register', 'form': form})


def forgotpassword(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = request.POST['email']

            user = User.objects.get(email=email)

            if UserToken.objects.filter(user=user).exists():
                return HttpResponse("You just have requested reset password please check your email")

            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.username))

            usertoken = UserToken(
                user=user, token=token, expired_at=datetime.now() + timedelta(minutes=10))
            usertoken.save()

            reset_link = f"{settings.MY_HOST}/users/reset-password/{uidb64}/{token}/"

            send_mail("Password Reset Request", "You have requested to reset your password. Please click the link to reset password. This link gonna expired in 10 minutes. " +
                      reset_link, settings.EMAIL_HOST_USER, [email], fail_silently=False)

            return HttpResponse("Your request reset password already send, please check your email")
        else:
            return render(request, 'auth/forgot-password.html', {'title': "Forgot Password", 'form': form})

    context = {
        'title': 'Forgot Password',
        'form': ForgotPasswordForm
    }

    return render(request, 'auth/forgot-password.html', context)


def resetpassword(request, uidb64, token):
    if request.user.is_authenticated:
        return redirect("/")
    uidb64 = str(urlsafe_base64_decode(uidb64), 'utf-8')
    user = User.objects.get(username=uidb64)

    if UserToken.objects.filter(user=user, token=token).exists():
        usertoken = UserToken.objects.get(user=user)
        if datetime.now().replace(tzinfo=timezone.utc) > usertoken.expired_at:
            usertoken.delete()
            return HttpResponse("Token is expired")

        if user is not None and default_token_generator.check_token(user, token):
            return render(request, 'auth/reset-password.html', {'title': "Reset Password", 'form': ResetPasswordForm, 'user': user.username, 'host': settings.MY_HOST})
        else:
            return HttpResponseNotFound(render(request, 'pages/404.html'))
    return HttpResponseNotFound(render(request, 'pages/404.html'))


def resetpasswordchange(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        username = request.POST['user']
        newpassword = request.POST['newpassword']
        if form.is_valid():
            user = User.objects.get(username=username)
            user.set_password(newpassword)
            user.save()

            usertoken = UserToken.objects.get(user=user)
            usertoken.delete()

            login = authenticate(
                request, username=username, password=newpassword)

            if login is not None:
                login_process(request, login)

                messages.success(request, "Your password reset successfully")

                return redirect('/')

        else:
            return redirect(request.POST['path'])


@login_required
def changepassword(request):
    if request.method == "POST":
        getuser = User.objects.filter(username=request.user.username).get()
        password = request.POST['password']
        newpassword = request.POST['newpassword']
        confirmnewpassword = request.POST['confirmnewpassword']

        if password and newpassword and confirmnewpassword:
            if not getuser.check_password(password):
                messages.error(request, "Your password is not correct")
            else:
                if newpassword != confirmnewpassword:
                    messages.error(request, "Your password is not match")
                else:
                    getuser.set_password(newpassword)
                    getuser.save()
                    update_session_auth_hash(request, getuser)
                    messages.success(request, "Your password has change")
        return redirect('/users/settings/change-password/')

    context = {
        'title': 'Change Password',
        'form': ChangePasswordForm,
        'page': 'changepassword',
    }
    return render(request, 'account-settings.html', context)


@login_required
def edit(request):
    context = {
        'title': 'Edit Account',
        'page': 'editaccount',
    }
    return render(request, 'account-settings.html', context)


@login_required
def update(request):
    if request.method == "POST":
        username = request.POST['username']
        fullname = request.POST['fullname']
        email = request.POST['email']
        phone_number = request.POST['phone_number']

        getuser = User.objects.filter(username=request.user.username).get()
        getuser.username = username
        getuser.fullname = fullname
        getuser.email = email
        getuser.phone_number = phone_number
        getuser.save()

        return redirect('/users/settings/account/')
    return HttpResponseNotFound(render(request, 'pages/404.html'))


@login_required
@costumer_required
def other(request):
    context = {
        'title': "Other",
        'page': 'other',
        'form': DeleteUserForm
    }
    return render(request, 'account-settings.html', context)


@login_required
@costumer_required
def deleteaccount(request):
    if request.method == "POST":

        theme = False
        if 'is_dark' in request.session:
            theme = request.session['is_dark']

        username = request.POST['username']

        if username == request.user.username:
            logout_process(request)

            getuser = User.objects.get(username=username)
            getuser.delete()

            if theme == True:
                request.session['is_dark'] = True

            messages.success(request, "Your account is deleted. Good Bye")
            return redirect('/')

        else:
            messages.error(request, "Your username not match")
            return redirect('/users/settings/other/')

    else:
        return HttpResponseNotFound(render(request, 'pages/404.html'))
