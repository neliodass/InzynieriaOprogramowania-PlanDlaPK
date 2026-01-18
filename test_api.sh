#!/bin/bash

echo "Testing API with mock data..."
curl -X POST http://localhost:5000/schedule \
  -H "Content-Type: application/json" \
  -d @example_mock_request.json

echo -e "\n\nTesting API with custom data..."
curl -X POST http://localhost:5000/schedule \
  -H "Content-Type: application/json" \
  -d @example_custom_request.json

echo -e "\n\nTesting health endpoint..."
curl http://localhost:5000/health
echo ""

