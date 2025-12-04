#!/usr/bin/env python
"""Test GET signup page"""

import sys
import os
import traceback

sys.path.insert(0, os.path.dirname(__file__))

from app import create_app

app = create_app()
client = app.test_client()

print("Testing GET /signup...")
try:
    response = client.get('/signup')
    print(f"Status: {response.status_code}")
    if response.status_code != 200:
        print(f"Error response: {response.data.decode()[:1000]}")
except Exception as e:
    print(f"Exception: {e}")
    traceback.print_exc()
