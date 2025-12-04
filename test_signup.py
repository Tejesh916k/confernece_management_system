#!/usr/bin/env python
"""Test signup endpoint directly"""

import json
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app

# Create app
app = create_app()

# Create test client
client = app.test_client()

# Test signup
test_data = {
    'full_name': 'Test User',
    'username': 'testuser123',
    'email': 'test@gmail.com',
    'password': 'TestPassword123'
}

print("Testing signup endpoint...")
print(f"Data: {test_data}")

response = client.post(
    '/signup',
    data=json.dumps(test_data),
    content_type='application/json'
)

print(f"\nResponse Status: {response.status_code}")
print(f"Response Data: {response.get_json()}")
