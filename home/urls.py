from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name="home"),
    path('authenticate', views.authenticate, name="authenticate"),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('contact', views.contact, name="contact"),
    path('view-profile', views.view_profile, name="view-profile"),
    path('forget-password', views.forget_password, name='forget-password'),
    path('change-password/<token>/', views.change_password, name='change-password'),
]
