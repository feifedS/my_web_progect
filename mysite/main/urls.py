from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static


# from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="index"),
    ##path('main/', include('main.urls'))
    # path('login', views.login),
    # path('registration', views.registration),
    path('login', views.CustomLoginView.as_view(), name='login'),
    path('registration', views.CustomRegistrationView.as_view(),),
    # path('login', auth_views.LoginView.as_view(template_name='/login.html'), name='login'),
    path('logout', views.CustomLogoutView.as_view(),name='logout'),
    path('registration_mobile', views.registration_mobile),
    # path("service",views.service, name='service'),
    path("service",views.OrderView, name='service'),
    path("administration", views.administration, name="administration"),
    path('checkusername', views.check_username, name='check_username'),
    path("check_user",views.check_user,name="check_user"),
    #API URLS
    path('get_users', views.get_users),
    path('login_from_mobile', views.login_from_mobile),
    #PASWORD RESET URLS
    path('reset_password', views.CustomPasswordResetView.as_view(template_name="main/reset_pass/password_reset_form.html"), name="reset_password"),
    path('reset_password_sent', views.CustomPasswordResetDoneView.as_view(),name="password_reset_done"),
    path('reset/<uidb64>/<token>', views.CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete', views.CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),
   
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
