from django.forms import ModelForm
from .models import Input

class InputForm(ModelForm):
    class Meta:
        model = Input
        fields = ['hostel_name', 'title', 'type', 'description', 'city', 'rating']
        