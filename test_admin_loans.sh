#!/bin/bash

# Test script for the admin loans endpoint

# First, login as admin to get a token
echo "Logging in as admin..."
LOGIN_RESPONSE=$(curl -X POST "http://localhost:8003/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"identifier": "admin@dpa.com", "password": "admin123"}' \
  -s)

echo "Login response: $LOGIN_RESPONSE"

# Extract the access token
TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.access_token')

if [ "$TOKEN" = "null" ] || [ -z "$TOKEN" ]; then
  echo "Failed to get admin token. Please check credentials."
  exit 1
fi

echo "Got admin token: ${TOKEN:0:20}..."

# Test the admin loans endpoint
echo -e "\nTesting GET /api/v1/admin/loans endpoint..."
curl -X GET "http://localhost:8003/api/v1/admin/loans?skip=0&limit=10" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -s | jq .

echo -e "\nEndpoint test complete!"
