from django.shortcuts import render

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