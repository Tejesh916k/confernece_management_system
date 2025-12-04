"""
Interactive MongoDB Atlas Configuration Wizard
Step-by-step guided setup
"""

import os
from urllib.parse import quote_plus

def print_banner(text):
    """Print banner text"""
    print(f"\n{'='*70}")
    print(f"  {text.center(68)}")
    print(f"{'='*70}\n")

def print_step(step_num, step_text):
    """Print step header"""
    print(f"\n{'─'*70}")
    print(f"STEP {step_num}: {step_text}")
    print(f"{'─'*70}\n")

def print_instructions(instructions):
    """Print detailed instructions"""
    for i, instruction in enumerate(instructions, 1):
        print(f"{i}. {instruction}")
    print()

def confirm_action(prompt):
    """Get user confirmation"""
    while True:
        response = input(f"\n{prompt} (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' or 'n'")

def get_input(prompt, default=None, required=True):
    """Get user input with validation"""
    while True:
        value = input(f"\n{prompt}").strip()
        
        if not value and default:
            return default
        elif not value and required:
            print("This field is required")
            continue
        else:
            return value

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        print("✗ Password must be at least 8 characters")
        return False
    if not any(c.isupper() for c in password):
        print("✗ Password must contain uppercase letters")
        return False
    if not any(c.isdigit() for c in password):
        print("✗ Password must contain numbers")
        return False
    print("✓ Password is strong")
    return True

def validate_connection_string(conn_string):
    """Validate connection string"""
    validations = [
        (conn_string.startswith('mongodb+srv://'), "Must start with 'mongodb+srv://'"),
        ('@' in conn_string, "Must contain '@'"),
        ('.mongodb.net' in conn_string, "Must contain '.mongodb.net'"),
    ]
    
    for check, msg in validations:
        if not check:
            print(f"✗ {msg}")
            return False
    
    print("✓ Connection string format is valid")
    return True

def step_1_account_setup():
    """Step 1: Account setup instructions"""
    print_step(1, "Account Setup")
    
    instructions = [
        "Go to https://www.mongodb.com/cloud/atlas",
        "Click 'Try Free' or 'Sign Up'",
        "Create account with email or social login",
        "Verify your email address",
        "Complete setup wizard",
    ]
    print_instructions(instructions)
    
    return confirm_action("Have you completed account setup?")

def step_2_cluster_creation():
    """Step 2: Cluster creation instructions"""
    print_step(2, "Create Database Cluster")
    
    instructions = [
        "Log in to MongoDB Atlas",
        "Click 'Build a Database'",
        "Select 'M0 Shared' (Free tier)",
        "Choose Cloud Provider (AWS recommended)",
        "Select Region (closest to you)",
        "Click 'Create Deployment'",
        "Wait 5-10 minutes for creation",
    ]
    print_instructions(instructions)
    
    return confirm_action("Is your cluster created and running?")

def step_3_create_database_user():
    """Step 3: Create database user"""
    print_step(3, "Create Database User")
    
    instructions = [
        "Go to 'Database Access' in left sidebar",
        "Click '+ Add New Database User'",
        "Select 'Password' authentication",
        "Username will be: conference_user",
        "Create a strong password",
    ]
    print_instructions(instructions)
    
    username = "conference_user"
    print(f"Username: {username}")
    
    while True:
        password = get_input("Enter a strong password: ", required=True)
        if validate_password(password):
            break
    
    confirm_pwd = get_input("Confirm password: ", required=True)
    
    if password != confirm_pwd:
        print("✗ Passwords don't match")
        return None
    
    print(f"\n✓ Database user ready")
    print(f"  Username: {username}")
    print(f"  Password: {'*' * len(password)}")
    
    return {'username': username, 'password': password}

def step_4_network_access():
    """Step 4: Network access setup"""
    print_step(4, "Configure Network Access")
    
    instructions = [
        "Go to 'Network Access' in left sidebar",
        "Click '+ Add IP Address'",
        "Choose one option:",
        "  Option A: 'Add Current IP Address' (recommended)",
        "  Option B: Add your server IP",
        "  Option C: Add 0.0.0.0/0 (testing only)",
    ]
    print_instructions(instructions)
    
    return confirm_action("Have you configured network access?")

def step_5_get_connection_string(db_user):
    """Step 5: Get connection string"""
    print_step(5, "Get Connection String")
    
    instructions = [
        "Go to 'Databases' section",
        "Click 'Connect' on your cluster",
        "Select 'Drivers'",
        "Copy the connection string",
    ]
    print_instructions(instructions)
    
    conn_string = get_input("Paste your connection string: ", required=True)
    
    while not validate_connection_string(conn_string):
        conn_string = get_input("Please paste a valid connection string: ", required=True)
    
    # Replace password placeholder
    if '<password>' in conn_string:
        conn_string = conn_string.replace('<password>', db_user['password'])
    
    # Add database name if not present
    if 'conference_db' not in conn_string:
        if '?' in conn_string:
            conn_string = conn_string.replace('?', '/conference_db?')
        else:
            conn_string += '/conference_db'
    
    return conn_string

def step_6_save_configuration(conn_string, db_user):
    """Step 6: Save configuration to .env"""
    print_step(6, "Save Configuration")
    
    env_content = f"""# MongoDB Atlas Configuration
MONGODB_URI={conn_string}
DATABASE_NAME=conference_db

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=change-this-in-production

# Server Configuration
HOST=localhost
PORT=5000
"""
    
    print("Configuration to save:")
    print(f"\n{env_content}\n")
    
    if confirm_action("Save this configuration to .env file?"):
        with open('.env', 'w') as f:
            f.write(env_content)
        print("\n✓ .env file created successfully")
        return True
    
    return False

def step_7_test_connection():
    """Step 7: Test connection"""
    print_step(7, "Test Connection")
    
    print("Running connection test...")
    print("\nExecute: python scripts/test_atlas_connection.py\n")
    
    return confirm_action("Ready to test connection?")

def main():
    """Run interactive setup wizard"""
    print_banner("MongoDB Atlas Configuration Wizard")
    
    print("This wizard will guide you through setting up MongoDB Atlas")
    print("for your Conference Management System\n")
    
    if not confirm_action("Continue with setup?"):
        print("\nSetup cancelled")
        return False
    
    # Step 1: Account Setup
    if not step_1_account_setup():
        print("\n✗ Please complete account setup first")
        return False
    
    # Step 2: Cluster Creation
    if not step_2_cluster_creation():
        print("\n✗ Please wait for cluster to be created")
        return False
    
    # Step 3: Create Database User
    db_user = step_3_create_database_user()
    if not db_user:
        print("\n✗ Failed to create database user")
        return False
    
    # Step 4: Network Access
    if not step_4_network_access():
        print("\n✗ Please configure network access")
        return False
    
    # Step 5: Get Connection String
    conn_string = step_5_get_connection_string(db_user)
    
    # Step 6: Save Configuration
    if not step_6_save_configuration(conn_string, db_user):
        print("\n✗ Configuration not saved")
        return False
    
    # Step 7: Test Connection
    if step_7_test_connection():
        print("\n" + "="*70)
        print("✓ Setup Complete! Your MongoDB Atlas is configured.")
        print("="*70)
        return True
    
    return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
