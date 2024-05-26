from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100,widget=forms.PasswordInput)

    

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(max_length=100,widget=forms.PasswordInput)
    re_password = forms.CharField(max_length=100,widget=forms.PasswordInput)