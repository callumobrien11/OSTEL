from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Hostel, User, Input
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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

class InputCreate(LoginRequiredMixin, CreateView):
    model = Input
    fields = ['user_name', 'hostel_name', 'title', 'type', 'description', 'city', 'rating', 'image']
    success_url = '/input/create/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class InputDetail(DetailView):
    model = Input

class InputUpdate(LoginRequiredMixin, UpdateView):
    model = Input
    fields = ['user_name', 'hostel_name', 'title', 'type', 'description', 'city', 'rating', 'image']

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
      return redirect('')
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