from django.urls import path
from .import views
urlpatterns = [
    path('', views.loginPage, name="login"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registrationPage, name="register"),
    path('dashboard/', views.dashPage, name="dash"),
]
