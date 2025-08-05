import pandas as pd
from celery import shared_task
from .models import Customer

@shared_task
def ingest_customer_data(file_path):
    df = pd.read_excel(file_path)
    for _, row in df.iterrows():
        try:
            Customer.objects.update_or_create(
                phone_number=row['Phone Number'],
                defaults={
                    'first_name': row['First Name'],
                    'last_name': row['Last Name'],
                    'monthly_salary': row['Monthly Salary'],
                    'approved_limit': row['Approved Limit'],
                    'current_debt': 0.0,
                }
            )
        except Exception as e:
            print(f"Failed to import customer: {row} -> {e}")

