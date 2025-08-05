# from django.contrib import admin
from .models import Customer


# @admin.register(Customer)
# class CustomerAdmin(admin.ModelAdmin):
#     list_display = ('first_name', 'last_name', 'phone_number', 'monthly_salary')




# # 2. VERIFY ADMIN URL IS SET
# # File: credit_approval/urls.py
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
from django.contrib import admin

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'first_name', 'last_name', 'phone_number', 'monthly_salary')
