from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import resolve_url
from django.views.generic import CreateView
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages 
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from functools import wraps
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
# CUSTOM MODULES
from .models import *
from .forms import *
from main.decorators import unauthenticated_user, allowed_users


def context(title, form):
    return({"title": title, "form": form})

def master_test_function(user):
    if user.role == user.MASTER:
        return True
    return False

def master_access_only():
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            print("AAAAAAAAAAA: ", request.user.role)
            if not master_test_function(request.user):
                return HttpResponse("You are not a student and \
                        you are not allowed to access this page !")
            return view(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def role_required(user, login_url=None):
    return user_passes_test(user.role == user.MASTER, login_url=login_url)


# Create your views here.
def index(request):
    print("index")
    return render(request, 'main/index.html', {"title": "Barbi Barbershop"})
    

def login(request):
    print("LOGIN")
    # if 'next' in request.POST:
    #                 return redirect(request.POST['next'])
    return render(request, 'main/login.html')


# def login(request):
#     nxt = request.GET.get("next", None)
#     url = '/admin/login/'

#     if nxt is not None:
#         url += '?next=' + nxt
#     return redirect(url)
# @unauthenticated_user
def registration(request):
    # if request.user.is_authenticated:
    #     print("regis")
    #     return render(request, 'main/index.html')
    # else:
    #     print("REgis")

    #     return render(request, 'main/registration.html')
    return render(request, 'main/registration.html')

@method_decorator(unauthenticated_user(), name='dispatch')
class CustomLoginView(LoginView):   
    template_name='main/login.html'
    print("custom HHHHHHHHHHH")
    
    def get_success_url(self):
        return resolve_url('index')


class CustomLogoutView(LogoutView):
    template_name = 'main/logout.html'
    
    def get_success_url(self):
        return resolve_url('logout')


class CustomRegistrationView(CreateView):
    
    template_name = 'main/registration.html'
    
    model = CustomUser
    @method_decorator(unauthenticated_user())
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
            role = 1,
            
            
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

# @master_access_only()
# @permission_required(service.can.view)

@allowed_users(allowed_roles=['customer'])
def service(request):
    return render(request,'main/service.html')

@allowed_users(allowed_roles=['administrator'])
def administration(request):
    return render(request,'main/administration.html')

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


class CustomPasswordResetView(PasswordResetView):
    # email_template_name= "main/reset_pass/password_reset_email.html"
    # subject_template_name = "main/reset_pass/password_reset_email.txt"
    # success_url = reverse_lazy("password_reset_done") 
    # template_name = "main/reset_pass/password_reset_form.html"
    def password_reset_request(self,request):
        if request.method == "POST":
            # password_reset_form = PasswordResetForm(request.POST)
            password_reset_form = "main/reset_pass/password_reset_form.html"
            if password_reset_form.is_valid():
                data = password_reset_form.cleaned_data['email']
                associated_users = User.objects.filter(Q(email=data))
                if associated_users.exists():
                    for user in associated_users:
                        subject = "Password Reset Requested"
                        email_template_name = "main/reset_pass/password_reset_email.txt"
                        c = {
                        "email":user.email,
                        'domain':'127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                        }
                        email = render_to_string(email_template_name, c)
                        try:
                            send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                        except BadHeaderError:

                            return HttpResponse('Invalid header found.')
                            
                        messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                        return redirect ("main:homepage")
                messages.error(request, 'An invalid email has been entered.')
        password_reset_form = PasswordResetForm()
        return render(request=request, template_name="main/reset_pass/password_reset_form.html", context={"password_reset_form":password_reset_form})
        password_reset_request 

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "main/reset_pass/password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "main/reset_pass/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")
    reset_url_token = 'set-password'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "main/reset_pass/password_reset_complete.html"


def OrderView(request):
    form= OrderForm()
    return render(request, "main/service.html", {"title": 'hello', "form": form})