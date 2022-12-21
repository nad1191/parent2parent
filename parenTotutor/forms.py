from django import forms
from .models import Info

class InfoForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
        attrs={
            "placeholder": "Help a parent...",
            "class": "textarea is-success is-medium",
        }
    ),
    label="",
)

    class Meta: 
        model = Info
        exclude = ("user", )
