from django.db import models
from customers.models import Customer

# This model represents a loan in the credit approval system.
# It includes fields for loan details such as loan ID, customer, loan amount, tenure,
# interest rate, monthly installment, EMIs paid on time, start date, and end date.
# The loan ID is the primary key and the customer field is a foreign key to the Customer model.

class Loan(models.Model):
    loan_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loan_amount = models.FloatField()
    tenure = models.IntegerField(help_text="Loan tenure in months")
    interest_rate = models.FloatField()
    monthly_installment = models.FloatField()
    emis_paid_on_time = models.IntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Loan {self.loan_id} for {self.customer}"

