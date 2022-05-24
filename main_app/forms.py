from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Input

class InputForm(ModelForm):
    class Meta:
        model = Input
        fields = ['hostel_name', 'title', 'type', 'description', 'city', 'rating']
        