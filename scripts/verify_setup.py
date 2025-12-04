"""
Verify complete conference management system setup
"""

import os
from dotenv import load_dotenv

load_dotenv()

def verify_setup():
    """Verify all components are properly configured"""
    
    print("\n" + "="*70)
    print("Conference Management System - Setup Verification")
    print("="*70)
    
    checks = []
    
    # Check 1: Environment Variables
    print("\n1. Environment Variables:")
    mongodb_uri = os.getenv('MONGODB_URI')
    if mongodb_uri and not '<' in mongodb_uri:
        print("   ✓ MONGODB_URI configured")
        checks.append(True)
    else:
        print("   ✗ MONGODB_URI not configured properly")
        checks.append(False)
    
    database_name = os.getenv('DATABASE_NAME')
    if database_name:
        print(f"   ✓ DATABASE_NAME: {database_name}")
        checks.append(True)
    else:
        print("   ✗ DATABASE_NAME not configured")
        checks.append(False)
    
    flask_env = os.getenv('FLASK_ENV')
    if flask_env:
        print(f"   ✓ FLASK_ENV: {flask_env}")
        checks.append(True)
    else:
        print("   ✗ FLASK_ENV not configured")
        checks.append(False)
    
    # Check 2: Required Packages
    print("\n2. Required Packages:")
    packages = {
        'flask': 'Flask',
        'mongoengine': 'MongoEngine',
        'pymongo': 'PyMongo',
        'dotenv': 'python-dotenv',
    }
    
    for import_name, package_name in packages.items():
        try:
            __import__(import_name)
            print(f"   ✓ {package_name} installed")
            checks.append(True)
        except ImportError:
            print(f"   ✗ {package_name} NOT installed")
            checks.append(False)
    
    # Check 3: Directory Structure
    print("\n3. Directory Structure:")
    required_dirs = [
        'static',
        'static/uploads',
        'config',
        'controllers',
        'models',
        'scripts',
    ]
    
    for directory in required_dirs:
        if os.path.isdir(directory):
            print(f"   ✓ {directory}/ exists")
            checks.append(True)
        else:
            print(f"   ✗ {directory}/ missing")
            checks.append(False)
    
    # Check 4: Required Files
    print("\n4. Required Files:")
    required_files = [
        '.env',
        'app.py',
        'config/database.py',
        'controllers/main_routes.py',
        'controllers/feature/upload_routes.py',
    ]
    
    for filepath in required_files:
        if os.path.isfile(filepath):
            print(f"   ✓ {filepath}")
            checks.append(True)
        else:
            print(f"   ✗ {filepath} missing")
            checks.append(False)
    
    # Summary
    print("\n" + "="*70)
    passed = sum(checks)
    total = len(checks)
    print(f"Setup Verification: {passed}/{total} checks passed")
    print("="*70)
    
    if passed == total:
        print("\n✓ All checks passed! Your application is ready to use.")
        print("\nNext steps:")
        print("  1. Open http://localhost:5000 in your browser")
        print("  2. Test creating conferences and sessions")
        print("  3. Register attendees")
        return True
    else:
        print("\n✗ Some checks failed. Please review the errors above.")
        return False

if __name__ == '__main__':
    verify_setup()
