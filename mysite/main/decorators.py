from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect

def unauthenticated_user():
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                print("ЗАРЕГЕСТРИРОВАН")
                return redirect('index')
                # return HttpResponseForbidden()
            else:
                print("NO ЗАРЕГЕСТРИРОВАН")
                return func(request, *args, **kwargs)
        return wrapper
    return decorator

def allowed_users(allowed_roles=[]):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            
            group = None
            if request.user.groups.exists():
                
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                print(f"ДОСТУП РАПРЕЩЕН{allowed_roles}")
                return func(request, *args, **kwargs)
            else:
                print(f"ДОСТУП РАПРЕЩЕН РОЛИ {group}, ДЛЯ ДОСТУПА НУЖНЫ РОЛИ{allowed_roles}" )
                # return HttpResponse("Вам не разрешается видеть эту страницу")
                return redirect('index')


            return func(request, *args, **kwargs)
        return wrapper
    return decorator