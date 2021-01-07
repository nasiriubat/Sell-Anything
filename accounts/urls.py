from django.urls import path
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView,\
    PasswordResetConfirmView, PasswordResetCompleteView
from .views import profile,register,confirmregister,userlogin,userlogout

urlpatterns = [
    path('login/', userlogin, name='login'),
    path('logout/',userlogout, name='logout'),
    path('register/', register, name='register'),
    path('register/confirm',confirmregister, name="confirmregister"),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('profile/', profile, name='profile'),
    
]
