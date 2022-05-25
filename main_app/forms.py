from django import forms
from django.forms import ModelChoiceField, ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Input
from django.core.validators import MaxValueValidator, MinValueValidator

TYPES = (
    ('Tip'),
    ('Recommendation'),
    ('Review')
)

class InputForm(forms.ModelForm):
    title = forms.CharField(max_length=50)
    type = forms.Select(choices=TYPES)
    city = forms.CharField(max_length=25)
    description = forms.CharField(max_length=1000)
    rating = forms.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )

    class Meta:
        model = Input
        exclude = ("user", )
        