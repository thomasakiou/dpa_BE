#!/bin/bash
# Verification script for loan description field

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'
PORT=8003

echo "Verifying Loan Description Field"
echo "================================"

# 1. Get admin token
echo -e "\n${GREEN}1. Getting admin token...${NC}"
TOKEN_RESPONSE=$(curl -s -X POST "http://localhost:$PORT/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "identifier": "admin@dpa.com",
    "password": "admin123"
  }')

TOKEN=$(echo $TOKEN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
  echo -e "${RED}Failed to get admin token. Ensure the server is running on port $PORT and admin exists.${NC}"
  exit 1
fi

echo -e "${GREEN}✓ Got admin token${NC}"

# 2. Apply for a loan with description
echo -e "\n${GREEN}2. Applying for a loan with description...${NC}"
USER_ID=1
DESC="Business expansion loan for retail store"
APPLY_RESPONSE=$(curl -s -X POST "http://localhost:$PORT/api/v1/loans/apply" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"user_id\": $USER_ID,
    \"loan_amount\": 500000.00,
    \"interest_rate\": 5.0,
    \"duration_months\": 12,
    \"description\": \"$DESC\"
  }")

echo "$APPLY_RESPONSE" | jq '.'

SAVED_DESC=$(echo "$APPLY_RESPONSE" | jq -r '.description')

if [ "$SAVED_DESC" = "$DESC" ]; then
  echo -e "${GREEN}✓ Successfully applied for loan with description!${NC}"
else
  echo -e "${RED}Failed to save/retrieve loan description.${NC}"
  exit 1
fi

# 3. Verify in all loans list
echo -e "\n${GREEN}3. Verifying description in all loans list...${NC}"
LIST_RESPONSE=$(curl -s -X GET "http://localhost:$PORT/api/v1/admin/loans" \
  -H "Authorization: Bearer $TOKEN")

LOAN_IN_LIST=$(echo "$LIST_RESPONSE" | jq -c ".[] | select(.description == \"$DESC\")")

if [ -n "$LOAN_IN_LIST" ]; then
  echo -e "${GREEN}✓ Found loan with correct description in admin list!${NC}"
else
  echo -e "${RED}Could not find loan with description in admin list.${NC}"
  exit 1
fi

echo -e "\n${GREEN}================================"${NC}
echo -e "${GREEN}Verification Complete (Loans)${NC}"
