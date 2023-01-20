from django.urls import path
from . import views

urlpatterns = [
    # ----------------------------------Website------------------------
    path('', views.index, name='manager-home'),
    path('menu/', views.menu, name='manager-menu'),
    path('news/', views.news, name='manager-news'),

    # ----------------------------------Orders------------------------
    path('carts/', views.carts, name='manager-carts'),
    path('carts/<str:token>', views.cartsdetail, name='manager-carts-detail'),

    path('orders/', views.orders, name='manager-orders'),
    path('orders/<str:token>', views.ordersdetail, name='manager-orders-detail'),

    # ----------------------------------Users------------------------
    path('users/', views.users, name="manager-users"),
    path('users/<str:username>', views.userdetail,  name="manager-users-detail"),
    path('users/update/', views.updateuser),
    path('users/edit/<str:username>', views.edituser, name="manager-users-edit"),

    # ----------------------------------Other------------------------
    path('contacts/', views.contacts, name="manager-contacts"),
    path('contacts/<str:id>', views.contactsdetail,
         name="manager-contacts-detail"),
    path('subscribers/', views.subscribers, name="manager-subscribers"),
    path('subscribers/edit/<str:id>', views.subscribersedit,
         name="manager-subscribers-edit"),

    # ----------------------------------Other------------------------
    path('about/', views.about, name="manager-about"),
    path('greeting/', views.greeting, name="manager-greeting"),

    # LOCATIONS
    path('locations/', views.locations, name="manager-locations"),
    path('locations/add/', views.addlocation, name="manager-locations-add"),
    path('locations/edit/<str:city>', views.editlocation,
         name="manager-locations-edit"),
    path('locations/edit/', views.updatelocation),
    path('locations/delete/', views.deletelocation),
]
