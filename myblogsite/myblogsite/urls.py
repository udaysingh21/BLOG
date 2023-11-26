"""
URL configuration for myblogsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include # include is used to include urls from other apps

from django.contrib.auth import views # this is used to import the views for login and logout from auth app in django

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include('blog.urls')),
    path('accounts/login/',views.LoginView.as_view(),name='login'),
    path('accounts/logout.html',views.LogoutView.as_view(),name='logout',kwargs={'next_page':'/'}), # kwargs is used to pass arguments to the view
    # next_page is used to redirect the user to the home page after logout
]
