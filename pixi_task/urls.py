"""pixi_task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from accounts.views import set_language, user_login
from django.conf import settings
from django.conf.urls.static import static
from training.views import home


urlpatterns = i18n_patterns(
    path("", home, name="home"),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("store/", include("training.urls", namespace="training")),
    path("set_language/<str:language>", set_language, name="set_language"),
    prefix_default_language=True,
)
