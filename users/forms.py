from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.core.validators import RegexValidator


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class PasswordChangeForm(forms.Form):
    new_password = forms.CharField(
        label="Enter your new password",
        widget=forms.PasswordInput,
        validators=[RegexValidator(r'^[a-zA-Z]{1}[a-zA-Z0-9]{5,9}$', message="Valid password start with letter, length between 6 and 10 characters")]
    )
