from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(widget=forms.PasswordInput, label='password')


class SignupForm(forms.Form):
    username = forms.CharField(label='Username:')
    first_name = forms.CharField(label='First name:')
    last_name = forms.CharField(label='Last name:')
    email = forms.EmailField(label='E-mail:')
    password = forms.CharField(widget=forms.PasswordInput, label='Password:')
    password_check = forms.CharField(widget=forms.PasswordInput, label='Confirm password:')

    def username_taken(self):
        try:
            user = User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError("This username is already taken. Please choose another.")

    def password_matching(self):
        if 'password' in self.cleaned_data and 'password_check' in self.cleaned_data:
            if self.cleaned_data['password_check'] != self.cleaned_data['password']:
                raise forms.ValidationError("The passwords are different.")


