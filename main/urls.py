from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path('album/', category_list, name='category_list'),
    path('category/<int:pk>/', category_detail, name='category_detail'),
    
    # Admin panel - Main dashboard
    path('admin-panel/', admin_dashboard, name='admin_dashboard'),
    
    # Flight management
    path('admin-panel/flights/add/', add_flight, name='add_flight'),
    path('admin-panel/flights/edit/<int:pk>/', edit_flight, name='edit_flight'),
    path('admin-panel/flights/delete/<int:pk>/', delete_flight, name='delete_flight'),
    
    # Contact requests management
    path('admin-panel/requests/delete/<int:pk>/', delete_request, name='delete_request'),
    
    # Category management
    path('admin-panel/categories/delete/<int:pk>/', delete_category, name='delete_category'),
    
    # Photo management
    path('admin-panel/categories/<int:category_id>/photos/', manage_photos, name='manage_photos'),
    path('admin-panel/photos/delete/<int:pk>/', delete_photo, name='delete_photo'),
    
    # Service management
    path('admin-panel/services/delete/<int:pk>/', delete_service, name='delete_service'),
    
    # About management
    path('admin-panel/about/', manage_about, name='manage_about'),
    
    path('admin-panel/categories/',manage_categories, name="manage_categories"),
    path('admin-panel/services/',manage_services, name="manage_services"),
    
    path('direktor/', director_view),
]
