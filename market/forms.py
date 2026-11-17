from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "image", "tags", "post_type"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Item Title"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Describe your item...", "rows": 5}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "tags": forms.TextInput(attrs={"class": "form-control", "id": "tagsInput", "placeholder": "Add tags then press Enter"}),
            "post_type": forms.RadioSelect(attrs={"class": "form-check-input"}),
        }
