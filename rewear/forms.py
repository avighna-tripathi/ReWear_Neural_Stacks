from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Item


class StyledAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data["email"].strip().lower()
        user.email = email
        user.username = email
        user.first_name = self.cleaned_data["first_name"].strip()
        user.last_name = self.cleaned_data["last_name"].strip()
        if commit:
            user.save()
        return user


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            "title",
            "description",
            "category",
            "item_type",
            "size",
            "condition",
            "tags",
            "points",
            "image",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
        }
