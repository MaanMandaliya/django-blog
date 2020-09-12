from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    firstname = forms.CharField(max_length=20)
    lastname = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username','firstname','lastname','email','password1','password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    firstname = forms.CharField(max_length=20)
    lastname = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username','firstname','lastname', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']