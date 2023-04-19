"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views
# from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('main/', include('main.urls')),
    path('admin/', admin.site.urls),
    
    # path('main/',include('django.contrib.auth.urls'))
    # path('registration_copy/',registration_copy, name = 'registration_copy')



    path('password/', auth_views.PasswordResetView.as_view(
        template_name='main/reset_pass/reset_password.html'), name="fgt"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='main/reset_pass/reset_password_sent.html'), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='main/reset_pass/password_reset_confirm.html'), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='main/reset_pass/password_reset_complete.html'), name="password_reset_complete"),
    
]
