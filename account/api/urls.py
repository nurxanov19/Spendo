from django.urls import path, include
from .views import AuthOneView, AuthTwoView, RegisterView, LoginView, LogoutView, ProfileViewApi

urlpatterns = [
    path('authone', AuthOneView.as_view(), name='auth_one'),
    path('authtwo', AuthTwoView.as_view(), name='auth_one'),
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('profile', ProfileViewApi.as_view(), name='profile'),
    path('', include('tracker.api.urls')),

]