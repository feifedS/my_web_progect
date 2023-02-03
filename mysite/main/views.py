from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import resolve_url
from django.views.generic import CreateView
from main.models import CustomUser
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
    print("HELLO")

    return render(request, 'main/index.html')

def login(request):
    print("HELLO")

    return render(request, 'main/login.html')
def registration(request):
    print("HELLO")

    return render(request, 'main/registration.html')


class CustomLoginView(LoginView):
    template_name='main/login.html'

    def get_success_url(self):
        return resolve_url('index')


class CustomLogoutView(LogoutView):
    template_name = 'main/logout.html'

    def get_success_url(self):
        return resolve_url('logout')


class CustomRegistrationView(CreateView):
    template_name = 'main/registration.html'
    model = CustomUser

    def get(self, request):
        return render(request, 'main/registration.html')

    def post(self, request):
        new_user = CustomUser()
        password = ""

        if request.POST.get("password1") != request.POST.get("password2"):
            return render(request, "main/registration.html")
        else:
            password = request.POST.get("password1")

        CustomUser.objects.create_user(
            username = request.POST.get("username"),
            password = password,
            email = request.POST.get("email"),
            age = request.POST.get("age"),
            first_name = request.POST.get("first_name"),
            last_name = request.POST.get("last_name"),
            gender_id = 1,
            phone_number = request.POST.get("phone_number"),
        )

        return render(request, "main/registration_success.html")

def get_users(request):
    users = CustomUser.objects.all()

    print(users)

    users = serializers.serialize('json', users)

    return JsonResponse(users, safe=False)

@csrf_exempt
def registration_mobile(request):
    print(request.POST.get("first_name"))
    print(request.POST.get("last_name"))
    print(request.POST.get("login"))
    print(request.POST.get("password"))

    return JsonResponse({"status": "ok"}, safe=False)



