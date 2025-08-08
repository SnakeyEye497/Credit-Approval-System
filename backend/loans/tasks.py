import pandas as pd
from celery import shared_task
from .models import Loan
from customers.models import Customer
from datetime import datetime

# This task ingests loan data from an Excel file and updates or creates Loan records in the database.
# It uses the pandas library to read the Excel file and processes each row to either update an existing loan
# or create a new one based on the loan ID.
# The task is designed to handle exceptions gracefully, logging any errors encountered during the import process.

@shared_task
def ingest_loan_data(file_path):
    df = pd.read_excel(file_path)
    for _, row in df.iterrows():
        try:
            customer = Customer.objects.get(customer_id=row['Customer ID'])
            Loan.objects.update_or_create(
                loan_id=row['Loan ID'],
                defaults={
                    'customer': customer,
                    'loan_amount': row['Loan Amount'],
                    'tenure': row['Tenure'],
                    'interest_rate': row['Interest Rate'],
                    'monthly_installment': row['Monthly payment'],
                    'emis_paid_on_time': row['EMIs paid on Time'],
                    'start_date': pd.to_datetime(row['Date of Approval']),
                    'end_date': pd.to_datetime(row['End Date']),
                }
            )
        except Exception as e:
            print(f"Failed to import loan: {row} -> {e}")

