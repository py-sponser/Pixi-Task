from django.urls import path
from training import views

app_name = "training"

urlpatterns = [
    path("cart/", views.cart, name="cart"),
    path("student/profile/", views.get_profile_info, name="get_profile_info"),
]
