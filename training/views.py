from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from training.models import *
import json
from django.http import JsonResponse
from accounts.decorators import restrict_customer, restrict_seller
# Create your views here.


@restrict_customer
def home(request):
    """Renders home page html file"""
    return render(request, "training/home.html")


@restrict_customer
def cart(request):
    return render(request, "training/cart.html")


@login_required(login_url="accounts:login")
def get_profile_info(request):
    """Getting Profile of current authenticated user"""
    return render(request, "training/profile.html")
