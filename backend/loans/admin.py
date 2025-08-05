from django.contrib import admin

# Register your models here.


# Do the same in backend/loans/admin.py for Loan model

from .models import Loan
@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('loan_id', 'customer', 'loan_amount', 'tenure')
