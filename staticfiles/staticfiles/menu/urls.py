from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='menu'),
    path('<str:menu>', views.menu, name="menu-detail"),

    # CRUD
    path('new/', views.new),
    path('create/', views.create),
    path('update/', views.update),
    path('delete/', views.delete),
    path('edit/<str:slug>', views.edit),
    path('checkslug/', views.checkslug),

    # RATING
    path('rate/', views.rating),
    path('rate/delete/', views.deleterate),
    path('rate/<str:menu>/', views.rate),

    # COMMENT CRUD
    path('comment/', views.comment),
    path('comment/edit/', views.commentedit),
    path('comment/update/', views.commentupdate),
    path('comment/delete/', views.commentdelete),
]
