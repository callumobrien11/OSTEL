from django.db import models
from django.urls import reverse
from django.forms import IntegerField
from django.contrib.auth.models import User

class Hostel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    city = models.CharField(max_length=100) # The longest city name in the world is 85 letters at the moment

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('hostel_details', kwargs={'hostel_id': self.id})

    class Meta:
        ordering = ['name']

TYPES = (
    ('1', 'Tip'),
    ('2', 'Recommendation'),
    ('3', 'Review')
)

class Input(models.Model):
    user_name = models.CharField(max_length=25)
    hostel_name = models.CharField(max_length=25)
    title = models.CharField(max_length=50)
    type = models.CharField(
        max_length=25,
        choices = TYPES,
        default=TYPES[0][0]
    )
    city = models.CharField(max_length=25)
    description = models.TextField(max_length=1000)
    rating = models.IntegerField()
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='hostel')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('input_details', kwargs={'input_id': self.id})
