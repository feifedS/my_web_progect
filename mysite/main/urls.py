from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name="index"),
    ##path('main/', include('main.urls'))
    # path('login', views.login),
    # path('registration', views.registration),
    path('login', views.CustomLoginView.as_view()),
    path('registration', views.CustomRegistrationView.as_view()),

    # path('logout/', name='logout'),

    # API URLS
    path('get_users', views.get_users),
    path('registration_mobile', views.registration_mobile),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
