from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Hostel, User, Input
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import InputForm
import uuid
import boto3
from .models import Photo


S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'ostel-bucket'

def home(request):
    return render(request, 'home.html')

# Hostel Views        
class HostelList(ListView):
    model = Hostel

def hostel_details(request, hostel_id):
    hostel = Hostel.objects.get(id=hostel_id)
    inputs = Input.objects.filter(hostel=hostel_id)
    return render(request, 'main_app/hostel_detail.html', { 'hostel': hostel , 'inputs': inputs})

class HostelCreate(LoginRequiredMixin, CreateView):
    model = Hostel
    fields = '__all__'
    success_url = '/hostels/create/'

class HostelUpdate(LoginRequiredMixin, UpdateView):
    model = Hostel
    fields = '__all__'

class HostelDelete(LoginRequiredMixin, DeleteView):
    model = Hostel
    success_url = '/hostels/'

# Input Views
@login_required
def input_list(request):
    inputs = Input.objects.filter(user=request.user)
    return render(request, 'main_app/input_list.html', { 'inputs': inputs })

@login_required
def input_create(request):
    input_form = InputForm()
    return render(request, 'main_app/input_form.html', {
        'input_form': input_form
    })

class InputDetail(DetailView):
    model = Input

class InputUpdate(LoginRequiredMixin, UpdateView):
    model = Input
    fields = ['hostel_name', 'title', 'type', 'description', 'city', 'rating']

class InputDelete(LoginRequiredMixin, DeleteView):
    model = Input
    success_url='/hostels/'

# User Views
def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('/')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class UserDetail(LoginRequiredMixin, DetailView):
    model = User

class UserUpdate(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name']

def add_photo(request, hostel_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to hostel_id 
            photo = Photo(url=url, hostel_id=hostel_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', hostel_id=hostel_id)


