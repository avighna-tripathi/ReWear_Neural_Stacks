from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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
    image = forms.ImageField(
        required=False,
        help_text="Upload a JPG, PNG, WEBP, or GIF image up to 5 MB.",
        widget=forms.ClearableFileInput(attrs={"accept": "image/*"}),
    )

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

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if not image:
            return image

        if image.size > 5 * 1024 * 1024:
            raise ValidationError("Image size must be 5 MB or smaller.")

        allowed_types = {"image/jpeg", "image/png", "image/webp", "image/gif"}
        if getattr(image, "content_type", "") not in allowed_types:
            raise ValidationError("Please upload a JPG, PNG, WEBP, or GIF image.")

        return image


class ShippingAddressForm(forms.Form):
    delivery_name = forms.CharField(max_length=120)
    delivery_phone = forms.CharField(max_length=30)
    delivery_line1 = forms.CharField(max_length=255, label="Address line 1")
    delivery_line2 = forms.CharField(max_length=255, required=False, label="Address line 2")
    delivery_city = forms.CharField(max_length=120)
    delivery_state = forms.CharField(max_length=120)
    delivery_postal_code = forms.CharField(max_length=20, label="Postal code")
    delivery_notes = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), required=False)


class MessageForm(forms.Form):
    body = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Write a message about sizing, pickup, or shipping..."}),
    )
