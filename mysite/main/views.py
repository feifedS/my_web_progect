
import json
from time import strptime
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import resolve_url
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages 
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from functools import wraps
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
# CUSTOM MODULES
from .models import Order, TypesOfServices, Status
from .models import *
from .forms import *
from main.decorators import unauthenticated_user, allowed_users
# from time import strftime as s
import datetime

import pytz
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView


from django.contrib.auth.mixins import LoginRequiredMixin
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
    
    def get_success_url(self):
        return resolve_url('index')


class CustomLogoutView(LogoutView):
    template_name = 'main/logout.html'
    
    def get_success_url(self):
        return resolve_url('logout')
# def OrderFormAPIView(request):
#     print("ddddddddddddddddddddddddddddddddd")
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
#         if form.is_valid():
#             print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
#             form.Status = 'В ожиданий'
#             order = form.save(commit=False)
#             order.customer = request.user.customuser
#             order.status = Status.objects.get(name='В ожиданий')
#             order.save()
#             print("ddd")
#             return redirect('index')


# class OrderFormAPIView(APIView):
#     def post(self, request):
#         # extract the `times_pick` value from the request data and convert to desired format
#         times_pick_str = request.data.get('times_pick')
#         timezone = pytz.timezone('Asia/Almaty')
#         times_pick = datetime.strptime(times_pick_str, '%d.%m.%Y %H:%M:%S')
#         times_pick = timezone.localize(times_pick)
#         request.data['times_pick'] = times_pick

#         # create the `OrderForm` instance and handle form submission
#         form = OrderForm(request.data)
#         if form.is_valid():
#             order = form.save(commit=False)
#             order.status = Status.objects.get(name='В ожидании')
#             order.customer = request.user.customuser
#             order.save()
#             return Response({'status': 'success', 'message': 'Order created successfully!'})
#         else:
#             return Response({'status': 'error', 'message': 'Invalid form data!'})



class OrderFormAPIView(CreateAPIView):
    def post(self, request):
        # extract the values from the request data
        print(request.POST)
        customer_id = request.user.customuser.id
        type_of_service_id = request.data.get("type_of_service")
        times_pick_str = request.data.get('times_pick')
        date_created = timezone.now()
        # convert the `times_pick` value to a `datetime` object with the correct timezone
        timezone_str = 'Asia/Almaty'  # set to the appropriate timezone
        timezonew = pytz.timezone(timezone_str)
        times_pick = strptime(times_pick_str, '%d.%m.%Y %H:%M:%S')
        times_pick = timezonew.localize(times_pick)
        
        # get the current time in the UTC timezone
        utc_now = datetime.utcnow()
        type_of_service = TypesOfServices.objects.get(name=request.data.get("type_of_service"))
        # convert the UTC time to the Asia/Almaty timezone
        # almaty_tz = pytz.timezone('Asia/Almaty')
        # almaty_now = utc_now.replace(tzinfo=pytz.utc).astimezone(almaty_tz)
        
        # create the `Order` object and save it
        Order.objects.create(
            customer_id=customer_id,
            type_of_service=type_of_service,
            date_created = date_created,
            status=Status.objects.get(name='В ожиданий'),
            times_pick=times_pick
        )
        
        return Response({'status': 'success', 'message': 'Order created successfully!'})
    
class BookingAPIView(CreateAPIView):
    def post(self, request):
        # extract the values from the request data
        customer_id = request.user.customuser.id
        date_str = request.data.get("date")
        date_obj = datetime.datetime.strptime(date_str, '%d.%m.%Y')
        date_id = date_obj.strftime('%Y-%m-%d')
        
        # date_id= request.data.get("date")
        time_id= request.data.get("time")
        barber_id= Barber.objects.get(name=request.data.get("barber")).user_id
        # barber_id = request.data.get("barber")
        service_id = TypesOfServices.objects.get(name=request.data.get("type_of_service")).id
        Booking.objects.create(
            customer_id=customer_id,
            date = date_id,
            time = time_id,
            barber_id = barber_id,
            service_id = service_id,
        )
        return Response({'status': 'success', 'message': 'Order created successfully!'})



class CustomRegistrationAPIView(CreateAPIView):
    model = CustomUser

    def post(self, request):
        print("PARAMETRY: %s"%request.data)
        password = ""
        if request.data.get("password1") != request.data.get("password2"):
            return render(request, "main/registration.html")
        else:
            password = request.data.get("password1")

        CustomUser.objects.create_user(
            username = request.data.get("username"),
            password = password,
            email = request.data.get("email"),
            age = request.data.get("age"),
            first_name = request.data.get("first_name"),
            last_name = request.data.get("last_name"),
            gender_id = 1,
            phone_number = request.data.get("phone_number"),
            role = 1,
        )

        return render(request, "main/registration_success.html")



# @login_required
# def profile(request):
#     user = get_object_or_404(CustomUser, pk=request.user.customuser.pk)
#     if request.method == 'POST':
#         # Update user's information based on the POST data
#         user.first_name = request.POST.get('first_name', user.first_name)
#         user.last_name = request.POST.get('last_name', user.last_name)
#         user.email = request.POST.get('email', user.email)
#         user.phone_number = request.POST.get('phone_number', user.phone_number)
#         user.save()
#         message = 'Profile updated successfully!'
#     else:
#         message = ''

#     context = {
#         'user': user,
#         'message': message,
#     }
#     return render(request, 'main/profile.html', context)

@login_required
# def profile(request):
#     user = get_object_or_404(CustomUser, pk=request.user.customuser.pk)

#     if request.method == 'POST':
#         # Check if the new password and confirm password match
#         new_password = request.POST.get('new_password1', '').strip()
#         confirm_password = request.POST.get('new_password2', '').strip()

#         if new_password and confirm_password and new_password == confirm_password:
#             # Set the user's new password
#             user.set_password(new_password)
#             user.save()
#             messages.success(request, 'Password updated successfully!')
#             return redirect('profile')

#         # Update user's information based on the POST data
#         user.first_name = request.POST.get('first_name', user.first_name)
#         user.last_name = request.POST.get('last_name', user.last_name)

#         email = request.POST.get('email', '').strip()
#         if not email:
#             messages.error(request, 'Email field cannot be empty!')
#             return redirect('profile')
#         user.email = email

#         phone_number = request.POST.get('phone_number', '').strip()
#         if CustomUser.objects.filter(phone_number=phone_number).exclude(pk=user.pk).exists():
#             messages.error(request, 'Number already exists in the database!')
#             return redirect('profile')
#         user.phone_number = phone_number

#         user.save()
#         messages.success(request, 'Profile updated successfully!')

#     context = {
#         'user': user,
#         'messages': messages,
#     }
#     return render(request, 'main/profile.html', context)
def profile(request):
    user = get_object_or_404(CustomUser, pk=request.user.customuser.pk)
    # print(request.POST)
    if request.method == 'POST':
        # Update user's information based on the POST data
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        current_password = request.POST.get('current_password', '').strip()
        if current_password:
    # Check if the current password matches the user's password in the database
            if user.check_password(current_password):
                # Get the new password and confirm password from the POST data
                new_password = request.POST.get('new_password1', '').strip()
                confirm_password = request.POST.get('new_password2', '').strip()

                # Check if the new password and confirm password match
                if new_password and confirm_password and new_password == confirm_password:
                    # Set the user's new password
                    user.set_password(new_password)
                    # Log the user out and redirect to the login page
                    user.save()
                    return redirect('logout')
                else:
                    messag = 'New password and confirm password fields must match!'
                    messages = ""
                    context = {
                        'user': user,
                        'messag': messag,
                        'messages':messages,
                    }
                    return render(request, 'main/profile.html', context)
            else:
                messag = 'Current password is incorrect!'
                messages = ""
                context = {
                    'user': user,
                    'messag': messag,
                    'messages':messages,
                }
                return render(request, 'main/profile.html', context) 
        email = request.POST.get('email', '').strip()  # Get the email from the POST data
        if not email:  # If email is empty, return an error message
            message = 'Email field cannot be empty!'
            messages = ""
            context = {
                'user': user,
                'message': message,
                'messages':messages,
            }
            return render(request, 'main/profile.html', context)

        # Check if the email already exists in the database
        if CustomUser.objects.filter(email=email).exclude(pk=user.pk).exists():
            message = 'Email already exists in the database!'
            messages = ""
            context = {
                'user': user,
                'message': message,
                'messages':messages,
            }
            return render(request, 'main/profile.html', context)

        # Update the user's email if it passes the validation
        user.email = email
        
        phone_number = request.POST.get('phone_number', '').strip()  # Get the phone number from the POST data
        if CustomUser.objects.filter(phone_number=phone_number).exclude(pk=user.pk).exists():
            message = 'Number already exists in the database!'
            messages = ""
            context = {
                'user': user,
                'message': message,
                'messages':messages,
            }
            return render(request, 'main/profile.html', context)
        if len(phone_number)<16:  # If phone number is empty, return an error message
            message = 'Phone number to shost'
            messages = ""
            context = {
                'user': user,
                'message': message,
                'messages':messages,
            }
            return render(request, 'main/profile.html', context)
        if not phone_number:  # If phone number is empty, return an error message
            message = 'Phone number field cannot be empty!'
            messages = ""
            context = {
                'user': user,
                'message': message,
                'messages':messages,
            }
            return render(request, 'main/profile.html', context)

        user.phone_number = phone_number  # Update the user's phone number
        # current_password = request.POST.get('current_password', '').strip()
        print(current_password)
    #     if current_password:
    # # Check if the current password matches the user's password in the database
    #         if user.check_password(current_password):
    #             # Get the new password and confirm password from the POST data
    #             new_password = request.POST.get('new_password1', '').strip()
    #             confirm_password = request.POST.get('new_password2', '').strip()

    #             # Check if the new password and confirm password match
    #             if new_password and confirm_password and new_password == confirm_password:
    #                 # Set the user's new password
    #                 user.set_password(new_password)
    #                 # Log the user out and redirect to the login page
    #                 user.save()
    #                 return redirect('logout')
    #             else:
    #                 message = 'New password and confirm password fields must match!'
    #                 context = {
    #                     'user': user,
    #                     'message': message,
    #                 }
    #                 return render(request, 'main/profile.html', context)
    #         else:
    #             message = 'Current password is incorrect!'
    #             context = {
    #                 'user': user,
    #                 'message': message,
    #             }
    #             return render(request, 'main/profile.html', context)

        user.save()  # Save the updated user object
        messages = 'Profile updated successfully!'
        message = ""
    else:
        message = ''
        messages = ''
    

    context = {
        'user': user,
        'messages':messages
    }
    return render(request, 'main/profile.html', context)
def userprofile(request):
    user = get_object_or_404(CustomUser, pk=request.user.customuser.pk)
    context = {
                        'user': user,
                        # 'message': message,
                    }
    return render(request, 'main/userprofile.html', context)


def check_phone_number(request):
    if request.method == "GET":
        phone_number = request.GET.get("phone_number")
        check = CustomUser.objects.filter(phone_number=phone_number).exists()
        if check:
            return HttpResponse("Exists")
        else:
            return HttpResponse("Not Exists")

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
    


# class ProfileUpdateView(View):
#     template_name = 'main/update_profile.html'

#     def get(self, request):
#         user = get_object_or_404(CustomUser, pk=request.user.customuser.pk)
#         context = {
#             'user': user,
#             'phone_number': user.phone_number,
#         }
#         return render(request, self.template_name, context)

#     def post(self, request):
#         user = request.user

#         # Update user's data
#         if request.POST.get('username'):
#             user.username = request.POST.get('username')
#         if request.POST.get('email'):
#             user.email = request.POST.get('email')
#         if request.POST.get('phone_number'):
#             user.phone_number = request.POST.get('phone_number')
#         if request.POST.get('age'):
#             user.age = request.POST.get('age')
#         if request.POST.get('gender'):
#             user.gender_id = request.POST.get('gender')
#         user.save()

#         messages.success(request, 'Profile updated successfully')
#         return redirect('profile')
   

# class ProfileView(LoginRequiredMixin, View):
#     """
#     View to display and update user's own profile information.
#     """
#     template_name = 'profile.html'

#     def get(self, request):
#         user = request.customuser.user
#         context = {
#             'user': user,
#         }
#         return render(request, self.template_name, context)

#     def post(self, request):
#         user = request.customuser.user
#         # Update user's information based on the POST data
#         user.first_name = request.POST.get('first_name', user.first_name)
#         user.last_name = request.POST.get('last_name', user.last_name)
#         user.email = request.POST.get('email', user.email)
#         user.phone_number = request.POST.get('phone_number', user.phone_number)
#         user.save()
#         context = {
#             'user': user,
#             'message': 'Profile updated successfully!',
#         }
#         return render(request, self.template_name, context)


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
    typesofservices = TypesOfServices.objects.all()
    return render(request,'main/administration.html',{'typesofservices':typesofservices} )

@allowed_users(allowed_roles=['administrator'])
def dashboard(request):
    orders=Booking.objects.all()
    customers=CustomUser.objects.all()
    context={"orders":orders,"customers":customers,}
    return render(request,'main/dashboard.html', context )

@allowed_users(allowed_roles=['administrator'])
def customer(request,user_ptr_id):
    customer=CustomUser.objects.get(id=user_ptr_id)
    orders = customer.booking_set.all()

    context = {"customer":customer,"orders":orders,}
    return render(request,'main/customer.html', context )

def order_form(request):
    
    form = OrderForm()
    customers=CustomUser.objects.all()
    
    if request.method == 'POST':
        
        # print("print post:",request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            
            form.save()
            return redirect("dashboard")
    context = {'form':form}
    return render(request,'main/order_form.html', context )


@login_required
def OrderFormView(request):
    print("ddddddddddddddddddddddddddddddddd")
    if request.method == 'POST':
        form = OrderForm(request.POST)
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        if form.is_valid():
            print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
            form.Status = 'В ожиданий'
            order = form.save(commit=False)
            order.customer = request.user.customuser
            order.status = Status.objects.get(name='В ожиданий')
            order.save()
            print("ddd")
            return redirect('index')
    else:
        print("88888888888888888888888888888888888888")
        form = OrderForm()
    return render(request, 'main/service.html', {'form': form})

# def OrderFormAPIView(request):
#     print("ddddddddddddddddddddddddddddddddd")
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
#         if form.is_valid():
#             print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
#             form.Status = 'В ожиданий'
#             order = form.save(commit=False)
#             order.customer = request.user.customuser
#             order.status = Status.objects.get(name='В ожиданий')
#             order.save()
#             print("ddd")
#             return redirect('index')
#     else:
#         print("88888888888888888888888888888888888888")
#         form = OrderForm()
#     return render(request, 'main/service.html', {'form': form})

def updateOrder(request, pk):
    order = Booking.objects.get(id=pk)
    form = BookinForm(instance=order)
    if request.method == 'POST':
        # print("print post:",request.POST)
        form = BookinForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    context = {'form':form}
    return render(request,'main/order_form.html', context )

def deleteOrder(request, pk):
    order = Booking.objects.get(id=pk)
    context = {"order":order,}
    if request.method=="POST":
        order.delete()
        return redirect("dashboard" )    
    return render(request,'main/delete.html', context )

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

def check_email(request):
    if request.method == "GET":
        email = request.GET["email"]
        check = CustomUser.objects.filter(email=email)
        if len(check) == 1:
            return HttpResponse("exists")
        else:
            return HttpResponse("not exists")
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


def appointment_confirmation(request):
    return render(request, 'main/appointment_confirmation.html')

# def book_appointment(request):
#     if request.method == 'POST':
#         form = AppointmentForm(request.POST)
#         if form.is_valid():
#             barber = form.cleaned_data['barber']
#             appointment_date = form.cleaned_data['appointment_date']
#             available_time_slots = AvailableTimeSlot.get_available_time_slots(barber, appointment_date)
#             return render(request, 'main/book_appointment.html', {'form': form, 'available_time_slots': available_time_slots})
            
        
#     else:
#         form = AppointmentForm(initial={'appointment_date': timezone.now().date()})
#     return render(request, 'main/book_appointment.html', {'form': form})
def booking_success(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    return render(request, 'booking/success.html', {'booking': booking})

def booking_error(request):
    return render(request, 'booking/error.html')

@login_required
def book(request,service_id=None, barber_id=None, date=None, time=None):
    if not all([service_id,barber_id, date, time]):
        # handle missing arguments error
        return render(request, 'booking/error.html')
    service = get_object_or_404(TypesOfServices, id=service_id)
    barber = get_object_or_404(Barber, user_id=barber_id)
    date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    time = datetime.datetime.strptime(time, '%H:%M:%S').time()

    if not Booking.objects.filter(service=service, barber=barber, date=date, time=time).exists():
        booking = Booking.objects.create(service=service,barber=barber, customer=request.user.customuser, date=date, time=time)
        return render(request, 'main/booking/success.html', {'booking': booking})

    return render(request, 'main/booking/error.html')

# def available_times(request):
#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             service = form.cleaned_data['service']
#             barber = form.cleaned_data['barber']
#             date = form.cleaned_data['date']
#             bookings = Booking.objects.filter(service=service,barber=barber, date=date).values_list('time', flat=True)

#             available_times = []
#             start_time = datetime.datetime.combine(date, datetime.time.min) + datetime.timedelta(hours=9)
#             end_time = datetime.datetime.combine(date, datetime.time.min) + datetime.timedelta(hours=18) 
#             while start_time < end_time:
#                 if start_time.time() not in bookings:
#                     available_times.append(start_time.time())
#                 start_time += datetime.timedelta(minutes=30)

#             context = {
#                 'service': service,
#                 'barber': barber,
#                 'date': date,
#                 'available_times': available_times
#             }

#             return render(request, 'main/booking/available_times.html', context)
#     else:
#         form = BookingForm()

#     context = {
#         'form': form
#     }

#     # if 'barber' in request.GET and 'date' in request.GET and 'time' in request.GET:
#     #     barber_id = request.GET['barber']
#     #     date = request.GET['date']
#     #     time = request.GET['time']
#     #     return redirect(reverse('book') + f'?barber={barber_id}&date={date}&time={time}')

#     return render(request, 'main/booking/book.html', context)



def available_times(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            service = form.cleaned_data['service']
            barber = form.cleaned_data['barber']
            date = form.cleaned_data['date']
            bookings = Booking.objects.filter(barber=barber, date=date).values_list('time', flat=True)
            available_times = []
            start_time = datetime.datetime.combine(date, datetime.time.min) + timedelta(hours=8.5)
            end_time = datetime.datetime.combine(date, datetime.time.min) + timedelta(hours=18)
            
            
            if datetime.datetime.now().date() == date and datetime.datetime.now().time() < end_time.time():
                start_time = max(start_time, datetime.datetime.now())
            
            while start_time < end_time:
                if start_time.time() not in bookings:
                    
                    rounded_time = datetime.time(start_time.hour, start_time.minute // 30 * 30)
                    available_times.append(rounded_time)
                start_time += timedelta(minutes=30)

            available_times = list(set(available_times) - set(bookings))
            available_times.sort()

            del available_times[0]
            print(available_times)
            for i in range(len(available_times)):
                available_times[i] = available_times[i].strftime('%H:%M:%S')
            available_times = json.dumps(available_times)    
            print(available_times)
            available_times = json.loads(available_times)
            print(available_times)
            context = {
                'service': service,
                'barber': barber,
                'date': date,
                'available_times': available_times
            }

            return render(request, 'main/booking/available_times.html', context)
    else:
        form = BookingForm()

    context = {
        'form': form
    }

    return render(request, 'main/booking/book.html', context)

        
