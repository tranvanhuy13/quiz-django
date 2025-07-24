from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.api_register, name="register"),   # POST: Register a new user
    path("login/", views.api_login, name="api_login"),        # POST: Log in user and return JSON response
    path("logout/", views.api_logout, name="api_logout"),     # POST or GET: Log out user
    path("", views.api_home, name="home"),                    # GET: Test or home endpoint (auth required)
]
