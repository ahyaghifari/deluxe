from django.shortcuts import render
from django.http import JsonResponse

def changetheme(request):
    if 'is_dark' in request.session:
        request.session['is_dark'] = not request.session.get('is_dark')
    else : 
        request.session['is_dark'] = True

    return JsonResponse({
        'confirm' : '200'
    })
