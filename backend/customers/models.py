from django.db import models

# This model represents a customer in the credit approval system.
# It includes fields for customer details such as ID, name, phone number, age, monthly salary,
# approved credit limit, and current debt. The customer ID is the primary key and the phone number is unique.
# The age field is optional (can be null or blank).
# The approved limit is calculated as 36 times the monthly salary, and the current debt defaults to 0.

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, unique=True)
    age = models.IntegerField(null=True, blank=True)
    monthly_salary = models.FloatField()
    approved_limit = models.IntegerField()
    current_debt = models.FloatField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

