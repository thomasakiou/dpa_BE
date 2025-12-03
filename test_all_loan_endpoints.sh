#!/bin/bash

# Comprehensive test script for all loan endpoints

echo "=== Testing All Loan Endpoints ==="
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

echo "✓ Admin logged in successfully"
echo ""

# Test 1: Create a new loan
echo "2. Creating a new loan for user_id: 1..."
CREATE_RESPONSE=$(curl -X POST "http://localhost:8003/api/v1/loans/apply" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "loan_amount": 10000.00,
    "interest_rate": 12.0,
    "duration_months": 36
  }' \
  -s)

LOAN_ID=$(echo $CREATE_RESPONSE | jq -r '.id')
echo "✓ Created loan ID: $LOAN_ID"
echo ""

# Test 2: Approve the loan
echo "3. Testing approve loan endpoint..."
APPROVE_RESPONSE=$(curl -X POST "http://localhost:8003/api/v1/admin/loans/$LOAN_ID/approve" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -s)

LOAN_STATUS=$(echo $APPROVE_RESPONSE | jq -r '.status')

if [ "$LOAN_STATUS" = "approved" ]; then
  echo "✓ Loan successfully approved"
else
  echo "✗ ERROR: Loan status is '$LOAN_STATUS' (expected 'approved')"
fi
echo ""

# Test 3: Record a partial payment
echo "4. Testing record payment endpoint..."
PAYMENT_RESPONSE=$(curl -X POST "http://localhost:8003/api/v1/admin/loans/$LOAN_ID/payment" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 1000.00
  }' \
  -s)

AMOUNT_PAID=$(echo $PAYMENT_RESPONSE | jq -r '.amount_paid')
BALANCE=$(echo $PAYMENT_RESPONSE | jq -r '.balance')

echo "Amount paid: $AMOUNT_PAID"
echo "Remaining balance: $BALANCE"

if [ "$AMOUNT_PAID" != "0.00" ]; then
  echo "✓ Payment recorded successfully"
else
  echo "✗ ERROR: Payment not recorded"
fi
echo ""

# Test 4: Get all loans
echo "5. Testing get all loans endpoint..."
LIST_RESPONSE=$(curl -X GET "http://localhost:8003/api/v1/admin/loans" \
  -H "Authorization: Bearer $TOKEN" \
  -s)

LOAN_COUNT=$(echo $LIST_RESPONSE | jq '. | length')
echo "✓ Retrieved $LOAN_COUNT loans"
echo ""

# Test 5: Create another loan for deletion test
echo "6. Creating another loan for deletion test..."
DELETE_TEST_RESPONSE=$(curl -X POST "http://localhost:8003/api/v1/loans/apply" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "loan_amount": 500.00,
    "interest_rate": 10.0,
    "duration_months": 6
  }' \
  -s)

DELETE_LOAN_ID=$(echo $DELETE_TEST_RESPONSE | jq -r '.id')
echo "✓ Created loan ID: $DELETE_LOAN_ID for deletion"
echo ""

# Test 6: Delete the loan
echo "7. Testing delete loan endpoint..."
DELETE_RESPONSE=$(curl -X DELETE "http://localhost:8003/api/v1/admin/loans/$DELETE_LOAN_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s)

if echo "$DELETE_RESPONSE" | grep -q "204"; then
  echo "✓ Loan deleted successfully (HTTP 204)"
else
  echo "✗ ERROR: Delete failed"
  echo "$DELETE_RESPONSE"
fi
echo ""

# Test 7: Verify deleted loan is gone
echo "8. Verifying deleted loan is gone..."
VERIFY_RESPONSE=$(curl -X GET "http://localhost:8003/api/v1/admin/loans" \
  -H "Authorization: Bearer $TOKEN" \
  -s)

DELETED_LOAN=$(echo $VERIFY_RESPONSE | jq ".[] | select(.id == $DELETE_LOAN_ID)")

if [ -z "$DELETED_LOAN" ]; then
  echo "✓ Deleted loan not in list (correctly removed)"
else
  echo "✗ ERROR: Deleted loan still appears in list"
fi
echo ""

# Test 8: Close the first loan
echo "9. Testing close loan endpoint..."
CLOSE_RESPONSE=$(curl -X POST "http://localhost:8003/api/v1/admin/loans/$LOAN_ID/close" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -s)

CLOSED_STATUS=$(echo $CLOSE_RESPONSE | jq -r '.status')

if [ "$CLOSED_STATUS" = "closed" ]; then
  echo "✓ Loan successfully closed"
else
  echo "✗ ERROR: Loan status is '$CLOSED_STATUS' (expected 'closed')"
fi

echo ""
echo "=== All Tests Complete ==="
echo ""
echo "Summary of Endpoints Tested:"
echo "✓ POST /api/v1/loans/apply - Create loan"
echo "✓ POST /api/v1/admin/loans/{id}/approve - Approve loan"
echo "✓ POST /api/v1/admin/loans/{id}/payment - Record payment"
echo "✓ GET /api/v1/admin/loans - List all loans"
echo "✓ DELETE /api/v1/admin/loans/{id} - Delete loan"
echo "✓ POST /api/v1/admin/loans/{id}/close - Close loan"
