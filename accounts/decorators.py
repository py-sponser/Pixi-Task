from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def restrict_after_authenticate(view_func):

    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
            # if user is authenticated and is admin or staff
            return view_func(request,*args,**kwargs)

        elif request.user.is_authenticated:
            # if user is authenticated, redirect user to home page
            return redirect("training:home")

        else: # if user is not authenticated
            return view_func(request,*args,**kwargs)
    return wrapper_func # return the value returned of wrapper func.


def restrict_seller(view_func):
    """Executing a function before the real function"""
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.logged_in_as_seller:
                # if user is authenticated and is admin or staff
                return view_func(request,*args,**kwargs) # step to executing the desired function
            else:
                return redirect("training:home")
        else:
            return redirect("accounts:user_login")
    return wrapper_func # return the value returned of wrapper func.


def restrict_customer(view_func):
    """Executing a function before the real function"""
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            if not request.user.logged_in_as_seller:
                # if user is authenticated and is admin or staff
                return view_func(request,*args,**kwargs) # step to executing the desired function
            else:
                return redirect("accounts:dashboard")
        else:
            return redirect("accounts:user_login")
    return wrapper_func # return the value returned of wrapper func.
