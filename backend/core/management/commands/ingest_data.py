from django.core.management.base import BaseCommand
from customers.tasks import ingest_customer_data
from loans.tasks import ingest_loan_data

#ingest excel data using celery
# File: credit_approval/backend/core/management/commands/ingest_data.py
class Command(BaseCommand):
    help = 'Ingest initial Excel data using Celery'

    def handle(self, *args, **kwargs):
        print("Queuing ingestion tasks...")
        ingest_customer_data.delay('/code/customer_data.xlsx')
        ingest_loan_data.delay('/code/loan_data.xlsx')
        print("Tasks dispatched to Celery.")

