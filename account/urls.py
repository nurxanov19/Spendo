from django.urls import path, include
from .views import RegisterView, LoginView, LogoutView, ProfileView, CustomPasswordResetView, SMSCodeVerifyView, \
    PasswordResetCompleteView

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    #PasswordResetCompleteView
)

urlpatterns = [
    path('register/',RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('<str:username>/profile/', ProfileView.as_view(), name='profile'),

] + [path('password-reset/', CustomPasswordResetView.as_view(), name='password-reset'),

    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),

    path('sms-code-verify/', SMSCodeVerifyView.as_view(), name='sms-code-verify'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #path('api', Main.as_view())
]


# ] + [
#     path('password-reset/', PasswordResetView.as_view(template_name='users/password_reset.html'),name='password-reset'),
#     path('password-reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name='password_reset_done'),
#     path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
#     path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),
# ]