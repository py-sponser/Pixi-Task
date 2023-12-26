from django.shortcuts import render, redirect
from training.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from accounts.decorators import restrict_after_authenticate, restrict_customer, restrict_seller
# Create your views here.
from accounts.utils import password_validation
import random
from django.utils.translation import gettext_lazy as _
from urllib.parse import urlparse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls.base import resolve, reverse
from django.urls.exceptions import Resolver404
from django.utils import translation


def set_language(request, language):
    for lang, _ in settings.LANGUAGES:
        translation.activate(lang)
        try:
            view = resolve(urlparse(request.META.get("HTTP_REFERER")).path)
        except Resolver404:
            view = None
        if view:
            break
    if view:
        translation.activate(language)
        next_url = reverse(f"{view.namespace}:{view.url_name}" if view.namespace else f"{view.url_name}",
                           args=view.args, kwargs=view.kwargs)
        response = HttpResponseRedirect(next_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    else:
        response = HttpResponseRedirect("/")
    return response


@restrict_seller
def dashboard(request):
    return render(request, "accounts/dashboard.html")


@restrict_after_authenticate
def user_login(request):
    """"Logging the user in"""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        is_seller = request.POST.get("is_seller")
        if email and password: # if username and password contain value
            user = authenticate(username=email, password=password) # authenticate the user, checking the username and password
            if user: # if user got authenticated (user is exist due to correct username and password especially)
                if user.is_active: # if the account is activated
                    login(request, user) # login the user in
                    if is_seller == "on" and hasattr(user, "seller"):
                        user.logged_in_as_seller = True
                        user.save()
                        return redirect("accounts:dashboard")
                    elif is_seller is None and hasattr(user, "customer"):
                        user.logged_in_as_seller = False
                        user.save()
                        return redirect("home")

                else: # if account is not activated
                    messages.error(request, "Account hasn't been activated yet.") # message error
                    return redirect("accounts:login") # redirect to same login page, message error will be displayed.

            else: # if user didn't get authenticated (user is not exist due to wrong password for example.)
                messages.error(request, "Email or Password is incorrect.") # message error
                return redirect("accounts:login") # redirect to same login page, message error will be displayed.

        else: # if username or password has not a value, return error message to them.
            messages.error(request, "Fields are not filled.") # message error
            return redirect("accounts:login") # redirect to same login page, message error will be displayed.
    else: # if request is not POST, it's GET
        return render(request, "accounts/login.html") # show the login.html page


@login_required(login_url="accounts:login") # A user can't logout except after logging in
def user_logout(request):
    """Logging user out"""
    if request.method == "POST": # if request method is POST
        logout(request) # logout the user
        return redirect("home") # return user to home page
    else: # if request is not POST
        return redirect("home") # don't logout the user, redirect him to home page


@restrict_after_authenticate  # A user can't access login page if he's already authenticated and loggedin
def register(request):
    """Register User Account"""
    departments = Department.objects.all() # get all existing department from database
    if request.method == "POST": # if request is POST
        id = random.randint(100,20000) # generate random id number from 100 - 19999
        first_name = request.POST.get("first_name") # get first_name from request POST data
        last_name = request.POST.get("last_name") # get last_name from request POST data
        family_name = request.POST.get("family_name") # get family_name from request POST data
        username = request.POST.get("username") # get username from request POST data
        email = request.POST.get("email") # get email from request POST data
        department = request.POST.get("department") # get email from request POST data
        password1 = request.POST.get("password1") # get password1 from request POST data
        password2 = request.POST.get("password2") # get password2 from request POST data
        if first_name and last_name and username and email and password1 and password2 and department != "Select Department": # if all fields have string value, and department has a true department name
            if password1 == password2: # if passwords are matched
                check = password_validation(password1) # check requirements for the password, password_validation function is in utils.py file.
                if check: # if password requirements are ok.
                    if not Department.objects.filter(name=department).exists(): # if given department is not in database
                        messages.error(request, f"No Department called {department}") # error message
                        return redirect("accounts:register") # redirect to same page of registration

                    if User.objects.filter(email=email).exists(): # checking if given email is already used
                        messages.error(request, f"This email is already taken.")  # error message
                        return redirect("accounts:register")  # redirect to same page of registration

                    else:

                        user = User.objects.create_user(id=id, username=username, first_name=first_name, last_name=last_name,
                                                        family_name=family_name, email=email, password=password1,
                                                        is_active=True) # create user account with provided data.

                        user.set_password(password1) # encrypting password
                        department = Department.objects.get(name=department) # getting department from database
                        user.department = department # adding user to that department
                        user.save() # saving user data
                        customer = Customer.objects.create(user=user)
                        seller = Seller.objects.create(user=user)
                        new_user = authenticate(username=email, password=password1) # authenticate the new user to his account
                        login(request, new_user) # logging him in
                        return redirect("home") # redirect him from registration page to home page

                else: # if password requirements are not ok.
                    messages.error(request,"[-] Password requirements are not applied.")  # error message
                    return redirect("accounts:register")   # redirect to same page of registration
            else: # if passwords are not matched.
                messages.error(request, "[-] Password is not match.")  # error message
                return redirect("accounts:register")   # redirect to same page of registration
        else: # if fields have not string value.
            messages.error(request, "[-] Please, Fill empty fields")  # error message
            return redirect("accounts:register")  # redirect to same page of registration
    else:
        requirements = [
            "[-] " + _("Password length shouldn't be fewer than 9.") + "\n",
            "[-] " + _("Password length shouldn't be greater than 15.") + "\n",
            "[-] " + _("Password should contain numbers.") + "\n",
            "[-] " + _("Password should have contain capitalized letters.") + "\n",
            "[-] " + _("Password should have lowercase letters.") + "\n",
            "[-] " + _("Password should have lowercase letters.") + "\n",
            "[-] " + _("Password should contain special characters, as !@#$%.. .") + "\n",
        ]
        # password requirements
        context = {"requirements": requirements, "departments":departments} # data to be sent to frontend
        return render(request, "accounts/register.html", context)  # return rendering the request, template and requiremnts to the page.
