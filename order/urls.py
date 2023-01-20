from django.urls import path
from . import views

urlpatterns = [

    path('', views.orders, name='orders'),
    path('pay/', views.pay, name='pay'),

    # CRUD
    path('create/', views.create),
    path('payment-method', views.payment),
    path('change-status/', views.changestatus),
    path('order-received/', views.orderreceived),
    path('order-cancel/', views.ordercancel),

    # MANAGER
    path('manager/', views.ordermanager, name="ordermanagermain"),
    path('manager/all/', views.ordermanagerall, name="ordermanagerall"),

    path('<str:token>', views.order, name='order-detail'),
]
