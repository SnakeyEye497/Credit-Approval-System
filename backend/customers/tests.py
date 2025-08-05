# customers/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from customers.models import Customer

class CustomerTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_customer(self):
        payload = {
            "first_name": "Swaraj",
            "last_name": "Pawar",
            "age": 25,
            "monthly_income": 50000,
            "phone_number": "9876543210"
        }
        response = self.client.post("/register", payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Customer.objects.get().approved_limit, 1800000)

