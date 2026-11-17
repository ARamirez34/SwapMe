from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("profile_pic", "bio")
        widgets = {
            "profile_pic": forms.FileInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Tell us about yourself...",
                "rows": 4,
                "maxlength": "250"
            }),
        }
