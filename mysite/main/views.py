from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import resolve_url
from django.views.generic import CreateView
from main.models import CustomUser
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages 
from django.contrib.auth.models import User 

from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    print("HELLO")
    
    return render(request, 'main/index.html')
    

# def login(request):
#     print("HELLO")
#     if 'next' in request.POST:
#                     return redirect(request.POST['next'])
#     # return render(request, 'main/login.html')


def login(request):
    nxt = request.GET.get("next", None)
    url = '/admin/login/'

    if nxt is not None:
        url += '?next=' + nxt
    return redirect(url)
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
        # if username==request.POST.get("username"):
        #     return render(request, "main/registration.html")
        # if User.objects.filter(username = 'username').first():
        #     messages.error(request, "This username is already taken")
        #     return render(request, "main/registration.html")
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
    print("ПРИШЛИ ДАННЫЕ С МОБИЛКИ")
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

@csrf_exempt
def check_username(request):
    print("FROM CLIENT: ", request.GET.get("checkUsername"))

    return JsonResponse({'exists': True})
    
@login_required(login_url='/main/login')
def service(request):
    return render(request,'main/service.html')


# апи который может принимать запросы извне
@csrf_exempt
def login_from_mobile(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    return JsonResponse({"success": True})

def check_user(request):
    if request.method=="GET":
        un = request.GET["username"]
        check = CustomUser.objects.filter(username=un)
        if len(check) == 1:
            return HttpResponse("Exists")
        else:
            return HttpResponse("Not Exists")
