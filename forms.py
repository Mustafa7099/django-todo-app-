from django.forms import ModelForm 
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User 
from django import forms
from django.contrib.auth.forms import UserCreationForm  , AuthenticationForm 
from .models import *

class SignupForm (UserCreationForm) : 
     
    class Meta:
        model = User  # No need for this in UserCreationForm unless you're adding NEW fields
        fields =  ['first_name' , 'last_name' , 'username', 'email', 'password1', 'password2']  # Include 'password' and the new 'password2'

    def clean(self):
        cleaned_data = super().clean()  # Call the parent's clean method
        password = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password != password2:
            raise forms.ValidationError("Passwords do not match")
        

        return cleaned_data
    

class TaskForm (ModelForm) : 
    class Meta : 
        model = Task
        fields = ['text']


# class LoginForm (AuthenticationForm) : 
    
#     username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
