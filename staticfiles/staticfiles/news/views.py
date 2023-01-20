from django.shortcuts import render, redirect
from django.http import JsonResponse
from news.models import News
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseNotFound
from .models import News
from django.contrib import messages
from django.template.defaultfilters import slugify
from .forms import NewsForm
# Create your views here.


def index(request):
    news = Paginator(News.objects.all().order_by('-created_at'), 4)
    page_number = request.GET.get('page')
    page_obj = news.get_page(page_number)
    context = {
        'title': "News",
        'news': page_obj
    }
    return render(request, 'news.html', context)


def news(request, slug):
    news = News.objects.filter(slug=slug).get()
    context = {
        'title': "News",
        'news': news
    }
    return render(request, 'news-detail.html', context)


@staff_member_required
def add(request):
    context = {
        'title': 'New News',
        'form': NewsForm
    }
    return render(request, 'news-add-form.html', context)


@staff_member_required
def create(request):
    if request.method == "POST":

        body = request.POST['body']

        form = NewsForm(request.POST)
        if form.is_valid():
            createnews = News(title=request.POST['title'], slug=slugify(
                request.POST['title']), author=request.POST['author'], image=request.POST['image'], body=request.POST['body'])
            createnews.save()

            if 'next' in request.POST:
                return redirect(request.POST['next'])

            return redirect('/news/')
        return render(request, 'news-add-form.html', {'title': 'New News', 'form': form, 'body': body})
    return HttpResponseNotFound(render(request, 'pages/404.html'))


@staff_member_required
def edit(request, slug):
    getnews = News.objects.filter(slug=slug).get()
    context = {
        'title': 'Edit News',
        'news': getnews
    }
    return render(request, 'news-edit-form.html', context)


@staff_member_required
def update(request):
    if request.method == "POST":
        oldslug = request.POST['slug']
        title = request.POST['title']
        slug = slugify(title)
        author = request.POST['author']
        image = request.POST['image']
        body = request.POST['body']

        getnews = News.objects.filter(slug=oldslug).get()
        getnews.title = title
        getnews.slug = slug
        getnews.author = author
        getnews.image = image
        getnews.body = body
        getnews.save()

        if 'next' in request.POST:
            return redirect(request.POST['next'])

        return redirect('/news/'+slug)
    return HttpResponseNotFound(render(request, 'pages/404.html'))


@staff_member_required
def delete(request):
    if request.method == "POST":
        slug = request.POST['news']
        getnews = News.objects.filter(slug=slug).get()
        getnews.delete()

        messages.success(request, f"{getnews.title} deleted successfully")

        if 'next' in request.POST:
            return redirect(request.POST['next'])
        return redirect('/news/')

    return HttpResponseNotFound(render(request, 'pages/404.html'))
