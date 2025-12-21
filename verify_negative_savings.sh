#!/bin/bash
# Verification script for negative savings payments

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'
PORT=8003

echo "Verifying Negative Savings Support"
echo "=================================="

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
  echo "Response: $TOKEN_RESPONSE"
  exit 1
fi

echo -e "${GREEN}✓ Got admin token${NC}"

# 2. Create a negative savings payment
echo -e "\n${GREEN}2. Creating a negative savings payment...${NC}"
USER_ID=1
CREATE_RESPONSE=$(curl -s -X POST "http://localhost:$PORT/api/v1/admin/savings" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"user_id\": $USER_ID,
    \"amount\": -500.00,
    \"type\": \"Other\",
    \"payment_date\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\",
    \"payment_month\": \"December\",
    \"description\": \"Debit adjustment test\"
  }")

echo "$CREATE_RESPONSE" | jq '.'

AMOUNT=$(echo "$CREATE_RESPONSE" | grep -o '"amount":[^,]*' | cut -d':' -f2 | tr -d ' ')

if [ "$AMOUNT" = "\"-500.00\"" ] || [ "$AMOUNT" = "-500.00" ] || [ "$AMOUNT" = "-500.0" ] || [ "$AMOUNT" = "-500" ]; then
  echo -e "${GREEN}✓ Successfully created negative savings payment!${NC}"
else
  echo -e "${RED}Failed to create negative savings payment or amount mismatch.${NC}"
  exit 1
fi

echo -e "\n${GREEN}==================================${NC}"
echo -e "${GREEN}Verification Complete (Savings)${NC}"
