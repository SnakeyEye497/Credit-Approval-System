from django.contrib import admin



# Register the Loan model in the Django admin interface

from .models import Loan
@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('loan_id', 'customer', 'loan_amount', 'tenure')
