from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='news'),

    path('new/', views.add),
    path('create/', views.create),
    path('edit/<str:slug>', views.edit),
    path('update/', views.update),
    path('delete/', views.delete),

    path('<str:slug>/', views.news, name='news-detail'),
]
