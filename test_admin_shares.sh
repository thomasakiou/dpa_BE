#!/bin/bash
# Test script for admin shares endpoints

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "Testing Admin Shares Endpoints"
echo "================================"

# Get admin token (assuming admin user exists)
echo -e "\n${GREEN}1. Getting admin token...${NC}"
TOKEN_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@dpa.com",
    "password": "admin123"
  }')

TOKEN=$(echo $TOKEN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
  echo -e "${RED}Failed to get admin token. Please ensure admin user exists.${NC}"
  echo "Response: $TOKEN_RESPONSE"
  exit 1
fi

echo -e "${GREEN}✓ Got admin token${NC}"

# Test 1: GET all shares
echo -e "\n${GREEN}2. Testing GET /api/v1/admin/shares${NC}"
curl -s -X GET "http://localhost:8000/api/v1/admin/shares" \
  -H "Authorization: Bearer $TOKEN" | jq '.'

# Test 2: POST create share
echo -e "\n${GREEN}3. Testing POST /api/v1/admin/shares${NC}"
CREATE_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/admin/shares" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "shares_count": 10,
    "share_value": 1000.00
  }')

echo $CREATE_RESPONSE | jq '.'
SHARE_ID=$(echo $CREATE_RESPONSE | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)

if [ -z "$SHARE_ID" ]; then
  echo -e "${RED}Failed to create share${NC}"
else
  echo -e "${GREEN}✓ Created share with ID: $SHARE_ID${NC}"
  
  # Test 3: PUT update share
  echo -e "\n${GREEN}4. Testing PUT /api/v1/admin/shares/$SHARE_ID${NC}"
  curl -s -X PUT "http://localhost:8000/api/v1/admin/shares/$SHARE_ID" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
      "shares_count": 15,
      "share_value": 1200.00
    }' | jq '.'
  
  # Test 4: DELETE share
  echo -e "\n${GREEN}5. Testing DELETE /api/v1/admin/shares/$SHARE_ID${NC}"
  DELETE_RESPONSE=$(curl -s -w "\n%{http_code}" -X DELETE "http://localhost:8000/api/v1/admin/shares/$SHARE_ID" \
    -H "Authorization: Bearer $TOKEN")
  
  HTTP_CODE=$(echo "$DELETE_RESPONSE" | tail -n1)
  if [ "$HTTP_CODE" = "204" ]; then
    echo -e "${GREEN}✓ Share deleted successfully (HTTP 204)${NC}"
  else
    echo -e "${RED}Failed to delete share (HTTP $HTTP_CODE)${NC}"
  fi
fi

echo -e "\n${GREEN}================================${NC}"
echo -e "${GREEN}Admin Shares Endpoints Test Complete${NC}"
