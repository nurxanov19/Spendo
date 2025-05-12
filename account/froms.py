from django.core.exceptions import ValidationError

from .models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate


class RegisterForm(forms.ModelForm):
    identifier = forms.CharField(label="Email or Phone")
    password2 = forms.CharField(widget=forms.PasswordInput, required=True, label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name','identifier', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

    def clean(self):
        cleaned_data = super().clean()
        identifier = cleaned_data.get('identifier')
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password2 and password and password != password2:
            raise ValidationError('Password and password2 is not ...., Retry')

        if not identifier:
            raise ValidationError('You must provide either email or phone')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if '@' in self.cleaned_data['identifier']:
            user.email = self.cleaned_data['identifier']
            user.phone = None
        elif self.cleaned_data['identifier'].startswith('+998' ):
            user.phone = self.cleaned_data['identifier']
            user.email = None

        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    identifier = forms.CharField(max_length=100, label="Email or Phone")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        identifier = cleaned_data.get('identifier')

        if '@' in identifier:
            cleaned_data['email'] = identifier
        elif identifier.startswith('+998'):
            cleaned_data['phone'] = identifier

        return cleaned_data


class ProfileForm(forms.ModelForm):
    identifier = forms.CharField(max_length=100, label="Email or Phone")

    class Meta:
        model = CustomUser
        fields = [ 'avatar', 'email', 'phone']
        widgets = {
            'avatar': forms.FileInput(attrs={'accept': 'users/'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        identifier = cleaned_data.get('identifier')

        if identifier:
            if '@' in identifier:
                cleaned_data['email'] = identifier
            elif identifier.startswith('+998'):
                cleaned_data['phone'] = identifier

        return cleaned_data


class CustomPasswordResetForm(forms.Form):
    identifier = forms.CharField(label="Email or Phone", max_length=100)

