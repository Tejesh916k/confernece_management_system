#!/usr/bin/env python
"""MongoDB Atlas Connection Diagnostics"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_connection():
    """Test MongoDB Atlas connection"""
    print("=" * 60)
    print("MongoDB Atlas Connection Diagnostics")
    print("=" * 60)
    
    # 1. Check .env file
    print("\n[1] Checking .env file...")
    mongodb_uri = os.getenv('MONGODB_URI')
    database_name = os.getenv('DATABASE_NAME')
    
    if not mongodb_uri:
        print("   ✗ MONGODB_URI not found in .env file")
        return False
    else:
        print("   ✓ MONGODB_URI found")
        # Mask password in display
        masked_uri = mongodb_uri.replace(mongodb_uri.split('@')[0].split('://')[1], 'user:****')
        print(f"     Connection string: {masked_uri[:80]}...")
    
    if not database_name:
        print("   ✗ DATABASE_NAME not found in .env file")
        return False
    else:
        print(f"   ✓ DATABASE_NAME: {database_name}")
    
    # 2. Validate URI format
    print("\n[2] Validating URI format...")
    if not mongodb_uri.startswith('mongodb+srv://'):
        print("   ✗ URI must start with 'mongodb+srv://'")
        return False
    else:
        print("   ✓ URI format is correct")
    
    if '<password>' in mongodb_uri or '<username>' in mongodb_uri:
        print("   ✗ URI contains placeholders - please replace them")
        return False
    else:
        print("   ✓ No placeholders in URI")
    
    # 3. Test actual connection
    print("\n[3] Testing MongoDB connection...")
    try:
        from mongoengine import connect, disconnect
        
        print("   Attempting to connect...")
        connection = connect(
            db=database_name,
            host=mongodb_uri,
            alias='test',
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000,
        )
        
        print("   ✓ Connection successful!")
        
        # Try to access the database
        from pymongo import MongoClient
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000, connectTimeoutMS=10000)
        server_info = client.server_info()
        print(f"   ✓ MongoDB Server Version: {server_info.get('version', 'Unknown')}")
        
        # List databases
        databases = client.list_database_names()
        print(f"   ✓ Available databases: {', '.join(databases[:5])}")
        if len(databases) > 5:
            print(f"     ... and {len(databases) - 5} more")
        
        # Check if conference_db exists
        if database_name in databases:
            print(f"   ✓ Database '{database_name}' exists")
            
            # List collections
            db = client[database_name]
            collections = db.list_collection_names()
            if collections:
                print(f"   ✓ Collections: {', '.join(collections)}")
            else:
                print(f"   ℹ Database '{database_name}' is empty (no collections yet)")
        else:
            print(f"   ℹ Database '{database_name}' does not exist yet (will be created on first write)")
        
        disconnect(alias='test')
        return True
        
    except Exception as e:
        print(f"   ✗ Connection failed: {str(e)}")
        print(f"\n   Error details:")
        print(f"   {type(e).__name__}: {e}")
        return False

def test_models():
    """Test if models can be loaded"""
    print("\n[4] Testing model imports...")
    try:
        from models.MongoUser import MongoUser
        print("   ✓ MongoUser model loaded successfully")
        return True
    except Exception as e:
        print(f"   ✗ Failed to load MongoUser: {e}")
        return False

def main():
    """Run all tests"""
    connection_ok = test_connection()
    models_ok = test_models()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if connection_ok and models_ok:
        print("✓ All checks passed! MongoDB is properly configured.")
        return 0
    else:
        print("✗ Some checks failed. Please review the errors above.")
        print("\nCommon issues:")
        print("1. Wrong password - Check your MongoDB Atlas password")
        print("2. IP not whitelisted - Add your IP in MongoDB Atlas Network Access")
        print("3. Database user doesn't exist - Create user in MongoDB Atlas Database Access")
        print("4. Connection string format - Must be: mongodb+srv://user:pass@cluster.../dbname?...")
        return 1

if __name__ == '__main__':
    sys.exit(main())
