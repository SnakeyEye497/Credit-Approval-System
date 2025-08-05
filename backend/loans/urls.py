from django.urls import path
from . import views
from .views import register_customer, check_eligibility

urlpatterns = [
 
    path('register', register_customer),
    path('check-eligibility', check_eligibility),
    path('view-loan/<int:loan_id>/', views.view_loan, name='view_loan'),
    path('view-loans/<int:customer_id>/', views.view_customer_loans, name='view_customer_loans'),
    path('create-loan', views.create_loan, name='create-loan'),
]
