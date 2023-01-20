from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='cart'),
    path('count/', views.count),
    path('checkout/', views.checkout, name='checkout'),
    # CRUD
    path('add/', views.add),
    path('qty/', views.quantity),
    path('deletemenu/', views.delete),
    path('deleteall/', views.deleteall),
]
