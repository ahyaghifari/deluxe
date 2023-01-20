from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='contact'),
    path('create/', views.create),
    path('all/', views.contacts, name="contacts"),

    # SUBSCRIBER
    path('subscribe/', views.subscribe),
    path('subscribers/update/', views.updatesubscriber),
    path('subscribers/delete/', views.deletesubscriber),
    path('unsubscribe/', views.unsubscribe),
         
    #contactdetail     
    path('<int:pk>', views.contactdetail),
]
