from django.shortcuts import render
from django.http import JsonResponse
from index.models import Locations, Greeting, About
from menu.models import Category
from news.models import News
from menu.models import Menu
from django.core.serializers import serialize


def index(request):
    news = News.objects.latest('created_at')
    greeting = Greeting.objects.get()
    category = Category.objects.all().values()
    locations = Locations.objects.all().values()
    context = {

        'title': "Home",
        'news': news,
        'greeting': greeting,
        'category': category,
        'locations': locations
    }
    return render(request, 'index.html', context)

def about(request):
    context = {
        'title': 'About',
        'about': About.objects.get()
    }
    return render(request, 'about.html', context)

def gfkfood(request):
    return render(request, 'gfk-food.html', {'title': 'gfk-food'})
