from django.urls import path
from . import views
from .views import register_customer, check_eligibility

# URL configuration for the loans app
# This file defines the URL patterns for the loans app, mapping URLs to their corresponding views.
# It includes endpoints for registering customers, checking eligibility, viewing loans, and creating loans. 

urlpatterns = [
 
    path('register', register_customer),
    path('check-eligibility', check_eligibility),
    path('view-loan/<int:loan_id>/', views.view_loan, name='view_loan'),
    path('view-loans/<int:customer_id>/', views.view_customer_loans, name='view_customer_loans'),
    path('create-loan', views.create_loan, name='create-loan'),
]
