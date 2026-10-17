from django.urls import path
from . import views

urlpatterns = [
    # Public & Auth Routes
    path('', views.home, name='home'),
    path('register/', views.register_org, name='register_org'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Private Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Campaigns
    path('campaigns/', views.campaign_list, name='campaign_list'),
    path('campaigns/<int:pk>/', views.campaign_detail, name='campaign_detail'),
    path('campaigns/<int:pk>/delete/', views.campaign_delete, name='campaign_delete'),

    # Donors
    path('donors/', views.donor_list, name='donor_list'),
    path('donors/<int:pk>/delete/', views.donor_delete, name='donor_delete'),

    # Donations
    path('donations/', views.donation_list, name='donation_list'),
    path('donations/<int:pk>/delete/', views.donation_delete, name='donation_delete'),

    # Organization Member Management (ORG_ADMIN only)
    path('organization/members/', views.organization_members, name='organization_members'),
]

