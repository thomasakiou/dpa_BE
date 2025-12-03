#!/bin/bash

# Test script for loan fixes

echo "=== Testing Loan Fixes ==="
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

# Test 1: Create loan for a specific user (user_id: 1)
echo "2. Testing loan creation for user_id: 1..."
CREATE_RESPONSE=$(curl -X POST "http://localhost:8003/api/v1/loans/apply" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "loan_amount": 5000.00,
    "interest_rate": 10.0,
    "duration_months": 24
  }' \
  -s)

echo "Create loan response:"
echo $CREATE_RESPONSE | jq .

LOAN_ID=$(echo $CREATE_RESPONSE | jq -r '.id')
LOAN_USER_ID=$(echo $CREATE_RESPONSE | jq -r '.user_id')

if [ "$LOAN_USER_ID" = "1" ]; then
  echo "✓ Loan correctly assigned to user_id: 1"
else
  echo "✗ ERROR: Loan assigned to user_id: $LOAN_USER_ID (expected 1)"
fi
echo ""

# Test 2: Close the loan
echo "3. Testing close loan endpoint for loan_id: $LOAN_ID..."
CLOSE_RESPONSE=$(curl -X POST "http://localhost:8003/api/v1/admin/loans/$LOAN_ID/close" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -s)

echo "Close loan response:"
echo $CLOSE_RESPONSE | jq .

LOAN_STATUS=$(echo $CLOSE_RESPONSE | jq -r '.status')

if [ "$LOAN_STATUS" = "closed" ]; then
  echo "✓ Loan successfully closed"
else
  echo "✗ ERROR: Loan status is '$LOAN_STATUS' (expected 'closed')"
fi
echo ""

# Test 3: Verify closed loan in list
echo "4. Verifying closed loan appears in loans list..."
LIST_RESPONSE=$(curl -X GET "http://localhost:8003/api/v1/admin/loans" \
  -H "Authorization: Bearer $TOKEN" \
  -s)

CLOSED_LOAN=$(echo $LIST_RESPONSE | jq ".[] | select(.id == $LOAN_ID)")
CLOSED_STATUS=$(echo $CLOSED_LOAN | jq -r '.status')

if [ "$CLOSED_STATUS" = "closed" ]; then
  echo "✓ Closed loan appears correctly in loans list"
else
  echo "✗ ERROR: Loan status in list is '$CLOSED_STATUS' (expected 'closed')"
fi

echo ""
echo "=== Test Complete ==="
