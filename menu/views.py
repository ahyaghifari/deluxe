from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseNotAllowed, HttpResponseNotFound, HttpResponse
from deluxe import settings
from menu.models import Category, Menu, Comment, Rate
from users.models import User
from contact.models import Subscribers
from menu.forms import MenuForm
from order.models import OrderMenu
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import IntegerField, Subquery, Count, OuterRef
from django.db.models.functions import Cast
from django.core.mail import send_mail, send_mass_mail, EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string


def setrating(menu):
    star5 = Rate.objects.filter(menu=menu, rating=5).count()
    star4 = Rate.objects.filter(menu=menu, rating=4).count()
    star3 = Rate.objects.filter(menu=menu, rating=3).count()
    star2 = Rate.objects.filter(menu=menu, rating=2).count()
    star1 = Rate.objects.filter(menu=menu, rating=1).count()

    score = (star5 * 5) + (star4 * 4) + (star3 * 3) + (star2 * 2) + (star1 * 1)
    responses = star5 + star4 + star3 + star2 + star1
    scoretotal = score / responses

    return scoretotal

# MENU


def index(request):
    menu = Menu.objects.filter(active=True).all()
    menu = menu.annotate(starrange=Cast('rating', IntegerField()))
    category = Category.objects.all().values()
    context = {
        'title': 'Menu',
        'category': category,
        'menu': menu
    }
    return render(request, 'menu.html', context)


def menu(request, menu):
    getmenu = Menu.objects.filter(slug=menu).get()
    menusold = OrderMenu.objects.filter(menu=getmenu).all().count()
    if getmenu.active is not False:
        stars = {}
        for i in range(1, 6, 1):
            stars[f"star{i}"] = Rate.objects.filter(
                menu=getmenu, rating=i).count()

        userrate = 0
        purchased = False
        rated = False

        if OrderMenu.objects.filter(order__user__username=request.user.username, menu__slug=menu, order__status__status="finished").exists():
            purchased = True
            if Rate.objects.filter(user__username=request.user.username, menu=getmenu).exists():
                rated = True
                userrate = Rate.objects.filter(
                    user__username=request.user.username, menu=getmenu).get().rating

        getcomments = Comment.objects.filter(
            menu__name=getmenu.name).all().order_by('-created_at')
        context = {
            'title': getmenu.name,
            'menu': getmenu,
            'sold': menusold,
            'purchased': purchased,
            'rated': rated,
            'userrate': userrate,
            'comments': getcomments,
            'starrange': range(int(getmenu.rating)),
            'stars': stars
        }
        return render(request, 'menu-detail.html', context)
    else:
        return HttpResponseNotFound(render(request, 'pages/404.html'))


@staff_member_required
def new(request):
    context = {
        'title': "New Menu",
        'form': MenuForm,
        'button': 'Create',
        'linkform': '/menu/create/'
    }
    return render(request, 'menu-form.html', context)


@staff_member_required
def create(request):
    if request.method == "POST":
        formset = MenuForm(request.POST)
        if formset.is_valid():
            formset.save()

            if 'announce' in request.POST:
                subject, from_email = 'New Menu', settings.EMAIL_HOST_USER
                getsubscribers = Subscribers.objects.filter(active=True).all()
                context = {
                    'name': request.POST['name'],
                    'image': request.POST['image'],
                    'desc': request.POST['description'],
                    'price': request.POST['price'],
                    'menulink': f"{settings.MY_HOST}/menu/{ request.POST['slug'] }",
                    'deluxelink': f"{settings.MY_HOST}",
                    'unsubscribelink': f"{settings.MY_HOST}/contact/unsubscribe/"
                }

                html_content = render_to_string(
                    'mails/newmenu.html', context)
                recepients = []
                for s in getsubscribers:
                    recepients.append(s.email)

                msg = EmailMultiAlternatives(
                    subject, html_content, from_email, recepients)
                msg.content_subtype = "html"
                # msg.attach_alternative(html_content, "text/html")
                msg.send()

            messages.success(
                request, f"Menu {request.POST['name']} created successfully")

            if 'next' in request.POST:
                return redirect(request.POST['next'])

            return redirect('/menu/')
    return HttpResponseNotFound(render(request, 'pages/404.html'))


@ staff_member_required
def edit(request, slug):
    menu = Menu.objects.filter(slug=slug).get()
    form = MenuForm(instance=menu)

    context = {
        'title': "Edit Menu",
        'form': form,
        'button': 'Update',
        'linkform': '/menu/update/',
        'menu': menu.slug
    }

    return render(request, 'menu-form.html', context)


@ staff_member_required
def update(request):
    if request.method == "POST":
        getmenu = request.POST['menu']
        menu = Menu.objects.get(slug=getmenu)
        formset = MenuForm(request.POST, instance=menu)
        if formset.is_valid():
            formset.save()

            if 'next' in request.POST:
                return redirect(request.POST['next'])

            return redirect(f"/menu/{request.POST['slug']}")

    return HttpResponseNotFound(render(request, 'pages/404.html'))


@ staff_member_required
def delete(request):
    if request.method == "POST":
        slug = request.POST['menu']
        menu = Menu.objects.filter(slug=slug).get()
        menu.delete()

        messages.success(request, f"{menu.name} is deleted successfully")

        if 'next' in request.POST:
            return redirect(request.POST['next'])

        return redirect('/menu/')
    return HttpResponseNotFound(render(request, 'pages/404.html'))


@ staff_member_required
def checkslug(request):
    val = request.GET['val']
    slug = slugify(val)

    if Menu.objects.filter(slug=slug).exists():
        confirm = "400"

        if 'slug' in request.GET:
            if slug == request.GET['slug']:
                confirm = "200"

    else:
        confirm = "200"

    return JsonResponse({
        'confirm': confirm,
        'slug': slug
    })


# RATING
@ login_required
def rate(request, menu):
    if OrderMenu.objects.filter(order__user__username=request.user.username, menu__slug=menu, order__status__status="finished").exists():
        userrate = 0

        getmenu = Menu.objects.get(slug=menu)
        if Rate.objects.filter(
                user__username=request.user.username, menu__slug=menu).exists():
            getrate = Rate.objects.filter(
                user__username=request.user.username, menu__slug=menu).get()
            userrate = getrate.rating

        context = {
            'title': f"Rate {getmenu.name}",
            'menu': getmenu,
            'userrate': userrate,
            'rating': int(getmenu.rating)
        }

        return render(request, 'menu-rate.html', context)

    return HttpResponseNotFound(render(request, 'pages/404.html'))


@login_required
def rating(request):
    if request.method == "POST":
        getmenu = request.POST['menu']
        menu = Menu.objects.filter(slug=getmenu).get()
        rating = request.POST['rating']

        if Rate.objects.filter(user__username=request.user.username, menu__slug=getmenu).exists():
            getrate = Rate.objects.filter(
                user__username=request.user.username, menu__slug=getmenu).get()
            getrate.rating = rating
            getrate.save()

        else:
            user = User.objects.filter(username=request.user.username).get()

            createrating = Rate(user=user, menu=menu, rating=rating)
            createrating.save()

        menu.rating = setrating(menu)
        menu.save()

        return redirect(request.POST['next'])
    return HttpResponseNotFound(render(request, 'pages/404.html'))


@login_required
def deleterate(request):
    if request.method == "POST":
        getmenu = request.POST['menu']
        menu = Menu.objects.filter(slug=getmenu).get()
        getrate = Rate.objects.filter(
            user__username=request.user.username, menu__slug=getmenu).get()
        getrate.delete()

        menu.rating = setrating(menu)
        menu.save()

        return redirect(request.POST['next'])

    return HttpResponseNotFound(render(request, 'pages/404.html'))


# COMMENT
@login_required
def comment(request):
    if request.method == "POST":
        comment = request.POST['comment']
        slug = request.POST['menu']
        menu = Menu.objects.filter(slug=slug).get()
        user = User.objects.filter(username=request.user.username).get()
        createcomment = Comment(user=user, menu=menu, comment=comment)
        createcomment.save()

        return redirect(request.POST['next'])

    return HttpResponseNotFound(render(request, 'pages/404.html'))


@login_required
def commentedit(request):
    id = request.GET['id']
    comment = Comment.objects.get(id=id)

    return JsonResponse({
        'confirm': '200',
        'comment': comment.comment
    })


@login_required
def commentupdate(request):
    if request.method == "POST":
        id = request.POST['id']
        comment = Comment.objects.filter(id=id).get()
        comment.comment = request.POST['comment']
        comment.save()
        return redirect(request.POST['next'])
    return HttpResponseNotFound(render(request, 'pages/404.html'))


@login_required
def commentdelete(request):
    if request.method == "POST":
        id = request.POST['id']
        next = request.POST['next']
        comment = Comment.objects.filter(id=id).get()
        comment.delete()

        return JsonResponse({
            'confirm': '200'
        })

    return HttpResponseNotFound(render(request, 'pages/404.html'))
