from django.shortcuts import redirect
from django.http import HttpResponse

def unauthorized_user(view_func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return view_func(request,*args,**kwargs)
    return wrapper

def allowed_users(allowed_roles = []):
    def decorator(view_func):
        def wrapper(request,*args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request,*args,**kwargs)
            else:
                if group=='hr':
                    return redirect('dashboard')
                elif group=='manager':
                    return redirect('manager')
                else:
                    return redirect('user')
        return wrapper
    return decorator