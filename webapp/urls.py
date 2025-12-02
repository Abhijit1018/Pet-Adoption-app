from django.urls import path
from . import views

# Add this line to define the application namespace
app_name = 'webapp'

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('adoption/', views.adoption_list, name='adoption_list'),
    path('lost/', views.lost_list, name='lost_list'),
    path('found/', views.found_list, name='found_list'),
    path('pet/<int:pet_id>/', views.pet_detail, name='pet_detail'),
    path('pet/<int:pet_id>/edit/', views.edit_pet, name='edit_pet'),
    
    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # User dashboard and pet management
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-pet/', views.redirect_to_register_pet, name='add_pet'),  # Redirect old URL to new system
    path('pet/<int:pet_id>/request-adoption/', views.request_adoption, name='request_adoption'),
    path('adoption-request/<int:request_id>/<str:action>/', views.manage_adoption_request, name='manage_adoption_request'),
    
    # Pet Registration Requests
    path('register-pet/', views.register_pet_request, name='register_pet_request'),
    path('registration-status/', views.registration_status, name='registration_status'),
    
    # Admin functionality
    path('admin-register/', views.admin_register_view, name='admin_register'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-pets/', views.admin_pet_management, name='admin_pets'),
    path('admin-users/', views.admin_user_management, name='admin_users'),
    path('admin-registration-requests/', views.admin_registration_requests, name='admin_registration_requests'),
    path('approve-registration/<int:request_id>/', views.approve_registration_request, name='approve_registration_request'),
    path('reject-registration/<int:request_id>/', views.reject_registration_request, name='reject_registration_request'),
    path('toggle-pet-status/<int:pet_id>/', views.toggle_pet_status, name='toggle_pet_status'),
    path('admin/run-auto-move/', views.run_auto_move_command, name='run_auto_move_command'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    # Avoid using the 'admin/' prefix to prevent collision with Django admin URLs
    path('admin-chat/start/<int:user_id>/', views.admin_start_chat, name='admin_start_chat'),
    
    # Password Reset
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('password-reset-done/', views.password_reset_done, name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmViewClass.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', views.password_reset_complete, name='password_reset_complete'),
    # Notifications
    path('notifications/', views.notifications_list, name='notifications'),
    path('notifications/mark-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
]

