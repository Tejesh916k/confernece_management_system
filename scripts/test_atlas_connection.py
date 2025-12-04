"""
MongoDB Atlas Connection Test Script
Tests connectivity and validates configuration
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_header(text):
    """Print formatted header"""
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")

def check_env_variables():
    """Check if required environment variables are set"""
    print_header("Step 1: Checking Environment Variables")
    
    required_vars = ['MONGODB_URI', 'DATABASE_NAME']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            masked_value = value[:30] + '...' if len(value) > 30 else value
            print(f"✓ {var}: {masked_value}")
        else:
            print(f"✗ {var}: NOT SET")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n✗ Error: Missing variables: {', '.join(missing_vars)}")
        return False
    
    print(f"\n✓ All environment variables found")
    return True

def validate_connection_string():
    """Validate connection string format"""
    print_header("Step 2: Validating Connection String Format")
    
    conn_string = os.getenv('MONGODB_URI')
    
    checks = {
        'Starts with mongodb+srv://': conn_string.startswith('mongodb+srv://'),
        'Contains username:password': '@' in conn_string,
        'Contains .mongodb.net': '.mongodb.net' in conn_string,
        'Contains database name': 'conference_db' in conn_string or '/' in conn_string,
        'Contains retryWrites': 'retryWrites' in conn_string,
    }
    
    all_valid = True
    for check, result in checks.items():
        status = "✓" if result else "✗"
        print(f"{status} {check}")
        if not result:
            all_valid = False
    
    if all_valid:
        print(f"\n✓ Connection string format is valid")
    else:
        print(f"\n✗ Connection string has issues")
    
    return all_valid

def test_mongodb_connection():
    """Test actual MongoDB Atlas connection"""
    print_header("Step 3: Testing MongoDB Atlas Connection")
    
    try:
        from mongoengine import connect, disconnect
        
        conn_string = os.getenv('MONGODB_URI')
        db_name = os.getenv('DATABASE_NAME', 'conference_db')
        
        print(f"Attempting to connect...")
        print(f"Database: {db_name}")
        
        # Attempt connection
        connect(
            host=conn_string,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000
        )
        
        print(f"\n✓ Successfully connected to MongoDB Atlas!")
        
        # Test database operations
        test_database_operations()
        
        disconnect()
        return True
        
    except ImportError:
        print("✗ mongoengine not installed. Run: pip install mongoengine")
        return False
    except Exception as e:
        print(f"\n✗ Connection failed: {str(e)}")
        print(f"\nPossible causes:")
        print("  1. IP address not whitelisted in Network Access")
        print("  2. Invalid username or password")
        print("  3. Database user doesn't exist")
        print("  4. Cluster not running")
        print("  5. Network connectivity issue")
        return False

def test_database_operations():
    """Test basic database operations"""
    print(f"\nTesting database operations...")
    
    try:
        from mongoengine import Document, StringField
        
        # Define test document
        class TestDoc(Document):
            test_field = StringField()
            meta = {'collection': 'test_connection', 'db_alias': 'default'}
        
        # Create test collection
        test_doc = TestDoc(test_field='Connection Test')
        test_doc.save()
        print(f"✓ Created test document")
        
        # Read test data
        found_doc = TestDoc.objects.first()
        if found_doc:
            print(f"✓ Retrieved test document: {found_doc.test_field}")
        
        # Delete test data
        TestDoc.drop_collection()
        print(f"✓ Cleaned up test collection")
        
    except Exception as e:
        print(f"✗ Database operation failed: {e}")

def check_packages():
    """Check if required packages are installed"""
    print_header("Step 4: Checking Required Packages")
    
    required_packages = {
        'mongoengine': 'mongoengine',
        'pymongo': 'pymongo',
        'flask': 'Flask',
        'dotenv': 'python-dotenv',
    }
    
    all_installed = True
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"✓ {package_name} installed")
        except ImportError:
            print(f"✗ {package_name} NOT installed")
            all_installed = False
    
    if not all_installed:
        print(f"\nInstall missing packages: pip install -r requirements.txt")
    
    return all_installed

def print_summary(results):
    """Print test summary"""
    print_header("Test Summary")
    
    tests = {
        'Environment Variables': results.get('env_vars', False),
        'Connection String Format': results.get('conn_string', False),
        'Required Packages': results.get('packages', False),
        'MongoDB Atlas Connection': results.get('connection', False),
    }
    
    passed = sum(1 for v in tests.values() if v)
    total = len(tests)
    
    for test, result in tests.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print(f"\n✓ All tests passed! Your configuration is ready for deployment.")
        return True
    else:
        print(f"\n✗ Some tests failed. Please review the errors above.")
        return False

def main():
    """Run all tests"""
    print_header("MongoDB Atlas Connection Test")
    
    results = {}
    
    # Run checks
    results['env_vars'] = check_env_variables()
    results['conn_string'] = validate_connection_string()
    results['packages'] = check_packages()
    results['connection'] = test_mongodb_connection()
    
    # Print summary
    success = print_summary(results)
    
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
