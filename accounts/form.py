from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


# هنا تم عمل فورم بدون مودل
class UserActivateForm(forms.Form):
    code = forms.CharField(max_length=10)
    


