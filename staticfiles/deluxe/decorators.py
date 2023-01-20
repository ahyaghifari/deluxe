from django.shortcuts import redirect
from django.http import HttpResponseForbidden


def superuser_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    return wrapper


def ordermanager_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(name="OrderManager").exists():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    return wrapper


def costumer_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(name="Costumer").exists():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    return wrapper
