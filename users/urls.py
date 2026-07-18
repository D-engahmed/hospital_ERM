from django.urls import path
from .views import register, login_view, forgot_view, reset_view, logout_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('password-reset/', forgot_view, name='password-reset'),
    path('reset/<str:token>/', reset_view, name='reset'),
    path('logout/', logout_view, name='logout'),
]
