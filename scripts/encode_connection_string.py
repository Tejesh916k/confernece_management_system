"""
Helper script to properly encode MongoDB Atlas connection string
Fixes: "Username and password must be escaped according to RFC 3986"
"""

from urllib.parse import quote_plus

def encode_connection_string():
    """Encode username and password in connection string"""
    
    print("\n" + "="*70)
    print("MongoDB Atlas Connection String Encoder")
    print("="*70)
    
    print("\nEnter your MongoDB Atlas connection details:")
    print("-"*70)
    
    username = input("Username (e.g., tejeshkesanakurthy): ").strip()
    password = input("Password: ").strip()
    cluster = input("Cluster URL (e.g., cluster0.cnrtsld.mongodb.net): ").strip()
    database = input("Database name (default: conference_db): ").strip() or "conference_db"
    
    # URL encode username and password
    encoded_username = quote_plus(username)
    encoded_password = quote_plus(password)
    
    # Build connection string
    connection_string = (
        f"mongodb+srv://{encoded_username}:{encoded_password}@{cluster}/"
        f"{database}?retryWrites=true&w=majority&appName=Cluster0"
    )
    
    print("\n" + "="*70)
    print("Encoded Connection String:")
    print("="*70)
    print(connection_string)
    print("="*70)
    
    print("\nUpdate your .env file with:")
    print(f"\nMONGODB_URI={connection_string}")
    
    # Option to save to .env
    save_choice = input("\nSave to .env file? (y/n): ").strip().lower()
    if save_choice == 'y':
        update_env_file(connection_string, database)

def update_env_file(connection_string, database):
    """Update .env file with encoded connection string"""
    
    env_content = f"""# MongoDB Atlas Configuration
MONGODB_URI={connection_string}
DATABASE_NAME={database}

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-change-in-production

# Server Configuration
HOST=localhost
PORT=5000
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("\n✓ .env file updated successfully!")
        print("✓ Now run: python scripts/test_atlas_connection.py")
    except Exception as e:
        print(f"\n✗ Error saving .env file: {e}")

if __name__ == '__main__':
    encode_connection_string()
