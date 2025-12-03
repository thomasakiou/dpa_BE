#!/bin/bash
# Test script for admin password reset endpoint

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "Testing Admin Password Reset Endpoint"
echo "======================================"

# Get admin token (assuming admin user exists)
echo -e "\n${GREEN}1. Getting admin token...${NC}"
TOKEN_RESPONSE=$(curl -s -X POST "http://localhost:8003/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "identifier": "admin@dpa.com",
    "password": "admin123"
  }')

TOKEN=$(echo $TOKEN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
  echo -e "${RED}Failed to get admin token. Please ensure admin user exists.${NC}"
  echo "Response: $TOKEN_RESPONSE"
  exit 1
fi

echo -e "${GREEN}✓ Got admin token${NC}"

# Get a test user ID (get first user from the list)
echo -e "\n${GREEN}2. Getting test user...${NC}"
USERS_RESPONSE=$(curl -s -X GET "http://localhost:8003/api/v1/admin/users?limit=5" \
  -H "Authorization: Bearer $TOKEN")

echo "$USERS_RESPONSE" | jq '.'

# Extract first active user ID that is not the admin
USER_ID=$(echo $USERS_RESPONSE | jq -r '.[] | select(.role != "admin" and .status == "active") | .id' | head -1)

if [ -z "$USER_ID" ] || [ "$USER_ID" = "null" ]; then
  echo -e "${RED}No test user found. Creating a test user...${NC}"
  
  # Create a test user
  CREATE_USER_RESPONSE=$(curl -s -X POST "http://localhost:8003/api/v1/admin/users" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
      "member_id": "TEST001",
      "email": "testuser@dpa.com",
      "password": "oldpassword123",
      "full_name": "Test User",
      "phone": "1234567890",
      "role": "member"
    }')
  
  echo "$CREATE_USER_RESPONSE" | jq '.'
  USER_ID=$(echo $CREATE_USER_RESPONSE | jq -r '.id')
  
  if [ -z "$USER_ID" ] || [ "$USER_ID" = "null" ]; then
    echo -e "${RED}Failed to create test user${NC}"
    exit 1
  fi
  
  echo -e "${GREEN}✓ Created test user with ID: $USER_ID${NC}"
else
  echo -e "${GREEN}✓ Using user ID: $USER_ID${NC}"
fi

# Test: POST reset password
echo -e "\n${GREEN}3. Testing POST /api/v1/admin/users/$USER_ID/reset-password${NC}"
RESET_RESPONSE=$(curl -s -X POST "http://localhost:8003/api/v1/admin/users/$USER_ID/reset-password" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json")

echo "$RESET_RESPONSE" | jq '.'

# Extract new password
NEW_PASSWORD=$(echo $RESET_RESPONSE | jq -r '.new_password')
MESSAGE=$(echo $RESET_RESPONSE | jq -r '.message')

if [ -z "$NEW_PASSWORD" ] || [ "$NEW_PASSWORD" = "null" ]; then
  echo -e "${RED}Failed to reset password. No new_password in response.${NC}"
  exit 1
fi

echo -e "${GREEN}✓ Password reset successfully${NC}"
echo -e "${YELLOW}New password: $NEW_PASSWORD${NC}"
echo -e "${YELLOW}Message: $MESSAGE${NC}"

# Verify the new password works by attempting to login
echo -e "\n${GREEN}4. Verifying new password by attempting login...${NC}"
USER_EMAIL=$(curl -s -X GET "http://localhost:8003/api/v1/admin/users" \
  -H "Authorization: Bearer $TOKEN" | jq -r ".[] | select(.id == $USER_ID) | .email")

if [ -z "$USER_EMAIL" ] || [ "$USER_EMAIL" = "null" ]; then
  echo -e "${YELLOW}Could not retrieve user email for login verification${NC}"
else
  LOGIN_RESPONSE=$(curl -s -X POST "http://localhost:8003/api/v1/auth/login" \
    -H "Content-Type: application/json" \
    -d "{
      \"identifier\": \"$USER_EMAIL\",
      \"password\": \"$NEW_PASSWORD\"
    }")
  
  LOGIN_TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
  
  if [ -z "$LOGIN_TOKEN" ]; then
    echo -e "${RED}Failed to login with new password${NC}"
    echo "Response: $LOGIN_RESPONSE"
  else
    echo -e "${GREEN}✓ Successfully logged in with new password${NC}"
  fi
fi

echo -e "\n${GREEN}=====================================${NC}"
echo -e "${GREEN}Password Reset Endpoint Test Complete${NC}"
