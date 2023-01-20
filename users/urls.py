from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='user'),
    path('settings/account/', views.account),
    path('settings/account/edit/', views.edit),
    path('settings/account/update/', views.update),

    path('settings/address/', views.address),
    path('settings/address/new/', views.newaddress),
    path('settings/address/edit/<str:code>', views.editaddress),
    path('settings/address/update/', views.updateaddress),
    path('settings/address/delete/', views.deleteaddress),

    path('settings/change-password/', views.changepassword),

    path('settings/other/', views.other),
    path('settings/delete-account/', views.deleteaccount),
         
    # auth
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('forgot-password/', views.forgotpassword, name='forgotpassword'),
    path('reset-password/', views.resetpasswordchange),
    path('reset-password/<uidb64>/<token>/',
         views.resetpassword, name="reset-password")
]
