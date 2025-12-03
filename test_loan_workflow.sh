#!/bin/bash

# Test the complete loan workflow

echo "=== Testing Complete Loan Workflow ==="
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

# Step 1: Create loan (status: pending)
echo "2. Creating loan (status should be: pending)..."
CREATE_RESPONSE=$(curl -X POST "http://localhost:8003/api/v1/loans/apply" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "loan_amount": 15000.00,
    "interest_rate": 8.5,
    "duration_months": 48
  }' \
  -s)

LOAN_ID=$(echo $CREATE_RESPONSE | jq -r '.id')
STATUS=$(echo $CREATE_RESPONSE | jq -r '.status')

echo "Loan ID: $LOAN_ID"
echo "Status: $STATUS"

if [ "$STATUS" = "pending" ]; then
  echo "✓ Loan created with status: pending"
else
  echo "✗ ERROR: Expected 'pending', got '$STATUS'"
fi
echo ""

# Step 2: Approve loan (status: approved)
echo "3. Approving loan (status should be: approved)..."
APPROVE_RESPONSE=$(curl -X POST "http://localhost:8003/api/v1/admin/loans/$LOAN_ID/approve" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -s)

STATUS=$(echo $APPROVE_RESPONSE | jq -r '.status')
echo "Status: $STATUS"

if [ "$STATUS" = "approved" ]; then
  echo "✓ Loan approved with status: approved"
else
  echo "✗ ERROR: Expected 'approved', got '$STATUS'"
fi
echo ""

# Step 3: Disburse/Activate loan (status: active)
echo "4. Disbursing/Activating loan (status should be: active)..."
DISBURSE_RESPONSE=$(curl -X POST "http://localhost:8003/api/v1/admin/loans/$LOAN_ID/disburse" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -s)

STATUS=$(echo $DISBURSE_RESPONSE | jq -r '.status')
echo "Status: $STATUS"

if [ "$STATUS" = "active" ]; then
  echo "✓ Loan activated with status: active"
else
  echo "✗ ERROR: Expected 'active', got '$STATUS'"
fi
echo ""

# Step 4: Record partial payment (only works when active)
echo "5. Recording partial payment (only works when active)..."
PAYMENT_RESPONSE=$(curl -X POST "http://localhost:8003/api/v1/admin/loans/$LOAN_ID/payment" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 2000.00
  }' \
  -s)

AMOUNT_PAID=$(echo $PAYMENT_RESPONSE | jq -r '.amount_paid')
BALANCE=$(echo $PAYMENT_RESPONSE | jq -r '.balance')
STATUS=$(echo $PAYMENT_RESPONSE | jq -r '.status')

echo "Amount paid: $AMOUNT_PAID"
echo "Balance: $BALANCE"
echo "Status: $STATUS"

if [ "$AMOUNT_PAID" != "0.00" ]; then
  echo "✓ Partial payment recorded successfully"
else
  echo "✗ ERROR: Payment not recorded"
fi
echo ""

# Step 5: Close/Payoff loan (status: closed)
echo "6. Closing/Paying off loan (status should be: closed)..."
CLOSE_RESPONSE=$(curl -X POST "http://localhost:8003/api/v1/admin/loans/$LOAN_ID/close" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -s)

STATUS=$(echo $CLOSE_RESPONSE | jq -r '.status')
echo "Status: $STATUS"

if [ "$STATUS" = "closed" ]; then
  echo "✓ Loan closed with status: closed"
else
  echo "✗ ERROR: Expected 'closed', got '$STATUS'"
fi
echo ""

echo "=== Workflow Test Complete ==="
echo ""
echo "Complete Loan Lifecycle:"
echo "1. Created → pending ✓"
echo "2. Approved → approved ✓"
echo "3. Disbursed → active ✓"
echo "4. Partial payment → active (with reduced balance) ✓"
echo "5. Closed → closed ✓"
