#!/bin/bash

# Test payment on APPROVED loan

echo "=== Testing Payment on APPROVED Loan ==="
echo ""

# Login as admin
echo "1. Logging in as admin..."
LOGIN_RESPONSE=$(curl -X POST "http://localhost:8003/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"identifier": "admin@dpa.com", "password": "admin123"}' \
  -s)

TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.access_token')

if [ "$TOKEN" = "null" ] || [ -z "$TOKEN" ]; then
  echo "Failed to get admin token"
  exit 1
fi

echo "✓ Admin logged in"
echo ""

# Step 1: Create loan
echo "2. Creating loan..."
CREATE_RESPONSE=$(curl -X POST "http://localhost:8003/api/v1/loans/apply" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "loan_amount": 1000.00,
    "interest_rate": 5.0,
    "duration_months": 12
  }' \
  -s)

LOAN_ID=$(echo $CREATE_RESPONSE | jq -r '.id')
echo "Loan ID: $LOAN_ID"
echo ""

# Step 2: Approve loan
echo "3. Approving loan..."
curl -X POST "http://localhost:8003/api/v1/admin/loans/$LOAN_ID/approve" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -s > /dev/null
echo "✓ Loan approved"
echo ""

# Step 3: Record payment on APPROVED loan
echo "4. Recording payment on APPROVED loan..."
PAYMENT_RESPONSE=$(curl -X POST "http://localhost:8003/api/v1/admin/loans/$LOAN_ID/payment" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 100.00
  }' \
  -s)

AMOUNT_PAID=$(echo $PAYMENT_RESPONSE | jq -r '.amount_paid')
STATUS=$(echo $PAYMENT_RESPONSE | jq -r '.status')

echo "Amount paid: $AMOUNT_PAID"
echo "Status: $STATUS"

if [ "$AMOUNT_PAID" != "0.00" ] && [ "$AMOUNT_PAID" != "null" ]; then
  echo "✓ Payment recorded successfully on APPROVED loan"
else
  echo "✗ ERROR: Payment failed"
  echo $PAYMENT_RESPONSE
fi
