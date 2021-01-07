from django import forms
from django.db import models
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from Core.models import User



class UserUpdateForm(forms.ModelForm):
    email=forms.EmailField()

    class Meta :
        model = User
        fields = ['username','first_name','last_name','email','phone']




