from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def clean_role(self):
        role = self.cleaned_data['role']
        if role == 'worker':
            raise forms.ValidationError("Only superusers can create worker accounts.")
        return role

class CustomAuthenticationForm(AuthenticationForm):
    pass