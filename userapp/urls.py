from django.urls import path,include
from . import views

app_name="userapp"
urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('index/', views.index, name="index"),
    path('logout/', views.logout, name="logout"),
    path('password/', views.password, name='password'),
    path('sms/', views.sms, name="sms"),

]
