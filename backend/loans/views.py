from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Loan
from customers.models import Customer

# File: loans/views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from customers.models import Customer
from loans.models import Loan
import pandas as pd
from datetime import datetime, timedelta
import math


# View to handle loan-related operations
@api_view(['GET'])
def view_loan(request, loan_id):
    loan = get_object_or_404(Loan, loan_id=loan_id)
    customer = loan.customer
    return Response({
        "loan_id": loan.loan_id,
        "customer": {
            "id": customer.customer_id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "phone_number": customer.phone_number,
            "age": customer.age,
        },
        "loan_amount": loan.loan_amount,
        "interest_rate": loan.interest_rate,
        "monthly_installment": loan.monthly_installment,
        "tenure": loan.tenure
    })



# View to handle customer loans
@api_view(['GET'])
def view_customer_loans(request, customer_id):
    customer = get_object_or_404(Customer, customer_id=customer_id)
    loans = Loan.objects.filter(customer=customer)
    loan_data = []

    for loan in loans:
        repayments_left = loan.tenure - loan.emis_paid_on_time
        loan_data.append({
            "loan_id": loan.loan_id,
            "loan_amount": loan.loan_amount,
            "interest_rate": loan.interest_rate,
            "monthly_installment": loan.monthly_installment,
            "repayments_left": repayments_left
        })

    return Response(loan_data)





# Utility function to round to nearest lakh
def round_to_nearest_lakh(x):
    return int(round(x / 100000.0)) * 100000

# Register a customer
@api_view(['POST'])
def register_customer(request):
    data = request.data
    monthly_income = data.get("monthly_income")
    approved_limit = round_to_nearest_lakh(36 * monthly_income)

    customer = Customer.objects.create(
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        phone_number=data.get("phone_number"),
        age=data.get("age"),
        monthly_salary=monthly_income,
        approved_limit=approved_limit
    )

    return Response({
        "customer_id": customer.customer_id,
        "name": f"{customer.first_name} {customer.last_name}",
        "age": customer.age,
        "monthly_income": customer.monthly_salary,
        "approved_limit": customer.approved_limit,
        "phone_number": customer.phone_number
    })


# Check eligibility for a loan
@api_view(['POST'])
def check_eligibility(request):
    data = request.data
    customer_id = data.get("customer_id")
    loan_amount = float(data.get("loan_amount"))
    input_interest_rate = float(data.get("interest_rate"))
    tenure = int(data.get("tenure"))

    customer = get_object_or_404(Customer, customer_id=customer_id)
    loans = Loan.objects.filter(customer=customer)

    score = 100

    # Check 1: Past loans paid on time
    paid_on_time = sum([l.emis_paid_on_time for l in loans])
    total_emis = sum([l.tenure for l in loans])
    if total_emis:
        on_time_ratio = paid_on_time / total_emis
        score *= on_time_ratio

    # Check 2: No of past loans
    if loans.count() > 0:
        score -= 5

    # Check 3: Loan activity in current year
    current_year = datetime.now().year
    active_this_year = loans.filter(start_date__year=current_year).count()
    if active_this_year > 0:
        score -= 5

    # if loans.filter(date_of_approval_year=current_year).exists():
    #     score -= 5

    # Check 4: Total loan volume
    if sum([l.loan_amount for l in loans]) > 500000:
        score -= 10

    # Check 5: Current debt vs limit
    if customer.current_debt + loan_amount > customer.approved_limit:
        score = 0

    corrected_interest_rate = input_interest_rate
    if score > 50:
        approved = True
    elif 30 < score <= 50:
        if input_interest_rate < 12:
            corrected_interest_rate = 12
        approved = True
    elif 10 < score <= 30:
        if input_interest_rate < 16:
            corrected_interest_rate = 16
        approved = True
    else:
        approved = False

    # EMI calculation
    r = corrected_interest_rate / (12 * 100)
    monthly_installment = loan_amount * r * (1 + r) ** tenure / ((1 + r) ** tenure - 1)

    # Check EMI burden
    existing_emis = sum([
        l.loan_amount * (l.interest_rate / (12 * 100)) * (1 + (l.interest_rate / (12 * 100))) ** l.tenure
        / ((1 + (l.interest_rate / (12 * 100))) ** l.tenure - 1)
        for l in loans
    ])

    if (existing_emis + monthly_installment) > (0.5 * customer.monthly_salary):
        approved = False

    return Response({
        "customer_id": customer_id,
        "approval": approved,
        "interest_rate": input_interest_rate,
        "corrected_interest_rate": corrected_interest_rate,
        "tenure": tenure,
        "monthly_installment": round(monthly_installment, 2),
        "credit_score": round(score, 2)
    })


# Create a new loan
@api_view(['POST'])
def create_loan(request):
    data = request.data
    customer_id = data.get("customer_id")
    loan_amount = float(data.get("loan_amount"))
    input_interest_rate = float(data.get("interest_rate"))
    tenure = int(data.get("tenure"))

    customer = get_object_or_404(Customer, customer_id=customer_id)
    loans = Loan.objects.filter(customer=customer)

    # CREDIT SCORE LOGIC
    score = 100
    paid_on_time = sum([l.emis_paid_on_time for l in loans])
    total_emis = sum([l.tenure for l in loans])
    if total_emis:
        score *= (paid_on_time / total_emis)
    if loans.count() > 0:
        score -= 5
    if loans.filter(start_date__year=datetime.now().year).exists():
        score -= 5
    if sum([l.loan_amount for l in loans]) > 500000:
        score -= 10
    if customer.current_debt + loan_amount > customer.approved_limit:
        score = 0

    corrected_interest_rate = input_interest_rate
    approved = False

    if score > 50:
        approved = True
    elif 30 < score <= 50:
        approved = True
        if input_interest_rate < 12:
            corrected_interest_rate = 12
    elif 10 < score <= 30:
        approved = True
        if input_interest_rate < 16:
            corrected_interest_rate = 16

    monthly_installment = (
        (loan_amount * (corrected_interest_rate / 100) * ((1 + corrected_interest_rate / 100) ** tenure)) /
        (((1 + corrected_interest_rate / 100) ** tenure) - 1)
    )

    if monthly_installment * loans.count() > 0.5 * customer.monthly_salary:
        approved = False

    if approved:
        loan = Loan.objects.create(
            customer=customer,
            loan_amount=loan_amount,
            tenure=tenure,
            interest_rate=corrected_interest_rate,
            monthly_installment=round(monthly_installment, 2),
            emis_paid_on_time=0,
            start_date=datetime.now().date(),
            end_date=(datetime.now() + timedelta(days=30 * tenure)).date()
        )
        customer.current_debt += loan_amount
        customer.save()
        return Response({
            "loan_id": loan.loan_id,
            "customer_id": customer_id,
            "loan_approved": True,
            "message": "Loan approved",
            "monthly_installment": round(monthly_installment, 2)
        })
    else:
        return Response({
            "loan_id": None,
            "customer_id": customer_id,
            "loan_approved": False,
            "message": "Loan not approved due to eligibility criteria",
            "monthly_installment": round(monthly_installment, 2)
        })