from django.contrib import messages
from django.contrib.auth.hashers import identify_hasher
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode

from .models import CustomUser
from .froms import RegisterForm, LoginForm, ProfileForm, CustomPasswordResetForm
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from tracker.models import Income, Expense





class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'user/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'account.backends.EmailOrPhoneBackend'

            login(request, user)
            messages.success(request, "You registered successfully")
            return redirect('main')
        return render(request, 'user/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'user/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')

            if email:
                user = authenticate(request, email=email, password=password)
            elif phone:
                user = authenticate(request, phone=phone, password=password)
            else:
                user = None
            print(user)

            #user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                form.add_error(None, "Invalid credentials (email/phone or password)")

        return render(request, 'user/login.html', {'form': form})


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('register')


class ProfileView(View, LoginRequiredMixin):
    def get(self, request, username):
        user = get_object_or_404(CustomUser, username=username)
        form = ProfileForm(instance=user)

        income = Income.objects.filter(user=request.user)
        expense = Expense.objects.filter(user=request.user)
        activity = [{'type': 'income', 'obj': inc, 'created_at': inc.created_at, 'amount': inc.amount,
                        'category': inc.category} for inc in income
                   ] + [
                       {'type': 'expense', 'obj': exp, 'created_at': exp.created_at, 'amount': exp.amount,
                        'category': exp.category} for exp in expense  ]
        activity = sorted(activity, key=lambda x: x['created_at'], reverse=True)[:10]


        return render(request, 'profile.html', {'user': user, 'form': form, 'income': income, 'expense': expense,
                                                'activity': activity})

    def post(self, request, username):
        user = get_object_or_404(CustomUser, username=username)
        if request.user != user:
            messages.error(request, "You can only edit your own profile")
            return redirect('main')

        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
        else:
            messages.error(request, "Error updating profile. Please check the form.")
        return redirect('profile', username=user.username)


# class ChangePasswordView(PasswordChangeView):
#     form_class = PasswordChangeForm
#     success_url = reverse_lazy('users:password-change-done')
#     template_name = 'users/password_change_form.html'


import random

def send_sms_code_to_phone(phone):
    code = str(random.randint(100000, 999999))
    print(f"Send this code to {phone}: {code}")
    return code

User = get_user_model()


class CustomPasswordResetView(View):
    def get(self, request):
        form = CustomPasswordResetForm()
        return render(request, 'users/password_reset.html', {'form': form})

    def post(self, request):
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier']

            try:
                if '@' in identifier:
                    user = User.objects.get(email=identifier)

                    uidb64 = urlsafe_base64_encode(str(user.pk).encode())
                    token = default_token_generator.make_token(user)
                    request.session['uidb64'] = uidb64
                    request.session['token'] = token

                    reset_form = PasswordResetForm({'email': identifier})
                    if reset_form.is_valid():
                        reset_form.save(request=request)
                        messages.success(request, 'Check your email, link sent')
                        return redirect('password_reset_done')
                    else:
                        messages.error(request, 'Issue with sending reset email')
                        return render(request, 'users/password_reset.html', {'form': form})

                elif identifier.startswith('+998'):
                    print('Phone number identified, sending SMS code to:', identifier)
                    user = User.objects.get(phone=identifier)

                    uidb64 = urlsafe_base64_encode(str(user.pk).encode())
                    token = default_token_generator.make_token(user)
                    request.session['uidb64'] = uidb64
                    request.session['token'] = token

                    code = send_sms_code_to_phone(user.phone)
                    request.session['reset_user_id'] = user.id
                    request.session['sms_code'] = code
                    return redirect('sms-code-verify')

                else:
                    messages.error(request, 'Enter a valid email or phone')
            except User.DoesNotExist:
                messages.error(request, 'User not found')

        return render(request, 'users/password_reset.html', {'form': form})

class SMSCodeVerifyView(View):
    def get(self, request):
        return render(request, 'users/verify_code.html')

    def post(self, request):
        entered_code = request.POST.get('sms_code')
        stored_code = request.session.get('sms_code')

        if entered_code == stored_code:
            user_id = request.session.get('reset_user_id')
            user = User.objects.get(pk=user_id)

            uidb64 = request.session.get('uidb64')
            token = request.session.get('token')

            if default_token_generator.check_token(user, token):

                return redirect('password_reset_confirm', uidb64=uidb64, token=token)
            else:
                messages.error(request, 'Invalid token')
        else:
            messages.error(request, 'Invalid SMS code')

        return render(request, 'users/verify_code.html')



class PasswordResetCompleteView(TemplateView):
    template_name = 'users/password_reset_complete.html'
