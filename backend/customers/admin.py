# from django.contrib import admin
from .models import Customer


from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
]
from django.contrib import admin

# Register the Customer model in the Django admin interface
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'first_name', 'last_name', 'phone_number', 'monthly_salary')


