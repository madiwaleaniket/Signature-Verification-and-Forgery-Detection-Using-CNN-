from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path("", views.index, name= "home"),
    path("log_in", views.log_in, name= "log_in"),
    path("register", views.register, name= "register"),
    path("dashboard", views.dashboard, name= "dashboard"),
    path("sign_verify", views.sign_verify, name= "sign_verify"),
    path("results", views.results, name= "results"),
    path("log_out", views.log_out, name= "log_out"),
]
