from django.urls import path
from .import views
urlpatterns = [
    path('', views.loginPage, name="login"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registrationPage, name="register"),
    path('dashboard/', views.dashPage, name="dashboard"),
    path('configuration/', views.configurePage, name="configure"),
    path('device-test/', views.testPage, name="testing"),
    path('create_firewall/', views.createFirewall, name="create_firewall"),
    path('update_firewall/<str:pk>/', views.updateFirewall, name="update_firewall"),
    path('delete_firewall/<str:pk>/', views.deleteFirewall, name="delete_firewall"),
    #path('test_firewall/<str:pk>/', views.testFirewall, name="test_firewall"),
    path('send_ping/', views.pingSelectedFirewall, name="send_ping"),
]
