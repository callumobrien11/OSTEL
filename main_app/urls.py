from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Hostel URLs
    path('hostels/', views.HostelList.as_view(), name='hostel_index'),
    path('hostels/create/', views.HostelCreate.as_view(), name='hostel_create'),
    path('hostels/<int:hostel_id>/', views.hostel_details, name='hostel_details'),
    path('hostels/<int:hostel_id>/update/', views.HostelUpdate.as_view(), name='hostel_update'),
    path('hostels/<int:hostel_id>/delete/', views.HostelDelete.as_view(), name='hostel_delete'),

    # Input URLs
    path('input/', views.input_list, name='input_index'),
    path('input/create/', views.InputCreate.as_view(), name='input_create'),
    path('input/<int:input_id>/', views.InputDetail.as_view(), name='input_details'),
    path('input/<int:input_id>/update/', views.InputUpdate.as_view(), name='input_update'),
    path('input/<int:input_id>/delete/', views.InputDelete.as_view(), name='input_delete'),

    # User/Account URLs
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/<int:pk>/', views.UserDetail.as_view(), name='user_profile'),
    path('accounts/<int:pk>/edit/', views.UserUpdate.as_view(), name='user_profile_edit'),
]
