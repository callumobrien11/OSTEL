from django import views
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import InputForm
import uuid
import boto3
from .models import Hostel, User, Input, Photo


S3_BASE_URL = 'https://s3.ca-central-1.amazonaws.com/'
BUCKET = 'hostilehostel'

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
    success_url = '/hostels/'


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

# @login_required
# def input_create(request):
#     input_form = InputForm()
#     input_form.user = request.user
#     input_form.save()
#     return render(request, 'main_app/input_form.html', {
#         'input_form': input_form
#     })

@login_required
def input_create(request):
    if request.method == "POST":
        input_form = InputForm(request.POST)
        if input_form.is_valid():
            input = input_form.save(commit=False)
            input.user = request.user
            input.save()
            return redirect('input_create')
    input_form = InputForm()
    return render(request, 'main_app/input_form.html', { 'input_form': input_form })

class InputDetail(LoginRequiredMixin, DetailView):
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
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('/')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class UserDetail(LoginRequiredMixin, DetailView):
    model = User

class UserUpdate(LoginRequiredMixin, UpdateView):
    model = User

    fields = ['email', 'first_name', 'last_name']
    success_url= '/'

def add_photo(request, hostel_id, user_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, hostel_id=hostel_id, user_id=user_id)
            photo.save()
        except:
            print('An error occurred')
    return redirect('hostel_details', hostel_id=hostel_id)


