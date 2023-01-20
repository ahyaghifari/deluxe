"""deluxe URL Configuration
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from theme.views import changetheme

urlpatterns = [
    # path("admin/", admin.site.urls),
    path('', include('index.urls')),
    path('menu/', include('menu.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('news/', include('news.urls')),
    path('contact/', include('contact.urls')),
    path('users/', include('users.urls')),
    path('manager/', include('manager.urls')),
    path('changetheme/', changetheme),

]


def custom_404(request, exception):
    context = {
        'title': '404'
    }
    return render(request, 'pages/404.html', context=context, status=404)


handler404 = custom_404
