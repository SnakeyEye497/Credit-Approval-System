# # loans/tests.py

# from django.test import TestCase
# from rest_framework.test import APIClient
# from customers.models import Customer
# from loans.models import Loan

# class LoanEligibilityTest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.customer = Customer.objects.create(
#             first_name="Test",
#             last_name="User",
#             phone_number="1234567890",
#             age=30,
#             monthly_salary=50000,
#             approved_limit=1800000,
#             current_debt=0
#         )

#     def test_check_eligibility(self):
#         payload = {
#             "customer_id": self.customer.customer_id,
#             "loan_amount": 100000,
#             "interest_rate": 10,
#             "tenure": 12
#         }
#         response = self.client.post("/check-eligibility", payload, format='json')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("approval", response.data)



from django.test import TestCase
from rest_framework.test import APIClient
from customers.models import Customer
from loans.models import Loan

class LoanEndpointTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create test customer
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            phone_number="1234567890",
            age=30,
            monthly_salary=50000,
            approved_limit=1800000,  # 36 * salary
            current_debt=0
        )

        # Create loan for testing view endpoints
        self.loan = Loan.objects.create(
            customer=self.customer,
            loan_amount=300000,
            interest_rate=10,
            tenure=12,
            monthly_installment=26374.23,
            emis_paid_on_time=12,
            start_date="2024-01-01",
            end_date="2025-01-01"
        )

    def test_register_customer(self):
        response = self.client.post("/register", {
            "first_name": "Alice",
            "last_name": "Smith",
            "phone_number": "9876543210",
            "age": 28,
            "monthly_income": 60000
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("customer_id", response.data)

    def test_check_eligibility(self):
        response = self.client.post("/check-eligibility", {
            "customer_id": self.customer.customer_id,
            "loan_amount": 100000,
            "interest_rate": 12,
            "tenure": 12
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("approval", response.data)

    def test_create_loan(self):
        response = self.client.post("/create-loan", {
            "customer_id": self.customer.customer_id,
            "loan_amount": 100000,
            "interest_rate": 11,
            "tenure": 24
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("loan_approved", response.data)

    def test_view_single_loan(self):
        response = self.client.get(f"/view-loan/{self.loan.loan_id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["loan_id"], self.loan.loan_id)
        self.assertIn("customer", response.data)

    def test_view_customer_loans(self):
        response = self.client.get(f"/view-loans/{self.customer.customer_id}/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.data, list))
        self.assertEqual(response.data[0]["loan_id"], self.loan.loan_id)
