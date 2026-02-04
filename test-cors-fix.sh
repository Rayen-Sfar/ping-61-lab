#!/bin/bash

echo "╔══════════════════════════════════════════════════╗"
echo "║  TEST CORS FIX - Verify API Endpoints           ║"
echo "╚══════════════════════════════════════════════════╝"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "\n${CYAN}[1] Testing Health Endpoint...${NC}"
if curl -s http://localhost:8000/health | jq . > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Health OK${NC}"
else
    echo -e "${RED}❌ Health failed${NC}"
    exit 1
fi

echo -e "\n${CYAN}[2] Testing LDAP Login...${NC}"
RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/ldap-login \
    -H "Content-Type: application/json" \
    -d '{"username": "student1", "password": "password"}')

TOKEN=$(echo $RESPONSE | jq -r '.access_token' 2>/dev/null)

if [ -z "$TOKEN" ] || [ "$TOKEN" = "null" ]; then
    echo -e "${RED}❌ Login failed${NC}"
    echo "$RESPONSE" | jq . 2>/dev/null || echo "$RESPONSE"
    exit 1
else
    echo -e "${GREEN}✅ Login OK${NC}"
    echo -e "${YELLOW}Token: ${TOKEN:0:30}...${NC}"
fi

echo -e "\n${CYAN}[3] Testing GET /api/tp (no auth required)...${NC}"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/tp)
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ GET /api/tp: HTTP $HTTP_CODE${NC}"
    COUNT=$(curl -s http://localhost:8000/api/tp | jq 'length' 2>/dev/null || echo "0")
    echo -e "${YELLOW}TPs found: $COUNT${NC}"
else
    echo -e "${RED}❌ GET /api/tp: HTTP $HTTP_CODE${NC}"
fi

echo -e "\n${CYAN}[4] Testing GET /api/tp/1 (no auth required)...${NC}"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/tp/1)
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ GET /api/tp/1: HTTP $HTTP_CODE${NC}"
else
    echo -e "${RED}❌ GET /api/tp/1: HTTP $HTTP_CODE${NC}"
fi

echo -e "\n${CYAN}[5] Testing GET /api/tp/1/guacamole-access (requires JWT)...${NC}"
RESPONSE=$(curl -s -X GET http://localhost:8000/api/tp/1/guacamole-access \
    -H "Authorization: Bearer $TOKEN")

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X GET http://localhost:8000/api/tp/1/guacamole-access \
    -H "Authorization: Bearer $TOKEN")

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ Guacamole access: HTTP $HTTP_CODE${NC}"
    GUAC_URL=$(echo $RESPONSE | jq -r '.guacamole_url' 2>/dev/null)
    echo -e "${YELLOW}Guacamole URL: $GUAC_URL${NC}"
else
    echo -e "${RED}❌ Guacamole access: HTTP $HTTP_CODE${NC}"
    echo "$RESPONSE" | jq . 2>/dev/null || echo "$RESPONSE"
fi

echo -e "\n${CYAN}[6] Testing CORS preflight (OPTIONS /api/tp)...${NC}"
RESPONSE=$(curl -s -X OPTIONS http://localhost:8000/api/tp \
    -H "Origin: http://localhost:3000" \
    -H "Access-Control-Request-Method: GET" \
    -H "Access-Control-Request-Headers: Content-Type")

CORS_HEADER=$(curl -s -i -X OPTIONS http://localhost:8000/api/tp \
    -H "Origin: http://localhost:3000" \
    -H "Access-Control-Request-Method: GET" \
    -H "Access-Control-Request-Headers: Content-Type" 2>&1 | grep "Access-Control-Allow-Origin")

if [ ! -z "$CORS_HEADER" ]; then
    echo -e "${GREEN}✅ CORS preflight OK${NC}"
    echo -e "${YELLOW}$CORS_HEADER${NC}"
else
    echo -e "${RED}❌ CORS header missing${NC}"
fi

echo -e "\n╔══════════════════════════════════════════════════╗"
echo -e "║  Test Complete!                                 ║"
echo -e "╚══════════════════════════════════════════════════╝"
