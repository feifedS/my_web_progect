from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index),
    ##path('main/', include('main.urls'))
    path('login', views.login),
    path('registration', views.registration),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)