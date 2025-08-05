from django.db import models

# Create your models here.
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
    

