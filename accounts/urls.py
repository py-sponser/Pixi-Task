from django.urls import path
from accounts import views

app_name = "accounts"

urlpatterns = [
    path(f"login/", views.user_login, name="user_login"),
    path(f"register/", views.register, name="register"),
    path(f"logout/", views.user_logout, name="logout"),
    path(f"dashboard/", views.dashboard, name="dashboard")
]