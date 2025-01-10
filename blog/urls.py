from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegistrationView),
    path('login/', views.login_view),
    path('post/', views.post_creation),
    path('retrieve/',views.retrieve_all_post)
]