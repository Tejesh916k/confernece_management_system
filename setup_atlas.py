import os
from dotenv import load_dotenv

def setup_mongodb_atlas():
    """
    Step-by-step guide to set up MongoDB Atlas connection
    """
    print("=" * 60)
    print("MongoDB Atlas Setup Guide")
    print("=" * 60)
    
    print("\n1. Get your Connection String from Atlas:")
    print("   - Go to: https://cloud.mongodb.com/")
    print("   - Select your cluster")
    print("   - Click 'Connect'")
    print("   - Choose 'Drivers'")
    print("   - Copy the connection string")
    
    print("\n2. Format of connection string:")
    print("   mongodb+srv://username:password@cluster.mongodb.net/dbname")
    
    connection_string = input("\n3. Paste your connection string here: ").strip()
    
    if not connection_string:
        print("Error: Connection string cannot be empty")
        return False
    
    # Create .env file
    env_content = f"""# MongoDB Atlas Configuration
MONGODB_URI={connection_string}
DATABASE_NAME=conference_db

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production

# Server Configuration
HOST=localhost
PORT=5000
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("\n✓ .env file created successfully!")
    print("✓ Configuration saved")
    
    return True

def test_connection():
    """Test MongoDB Atlas connection"""
    load_dotenv()
    
    mongodb_uri = os.getenv('MONGODB_URI')
    
    if not mongodb_uri:
        print("Error: MONGODB_URI not found in .env file")
        return False
    
    try:
        from mongoengine import connect, disconnect
        print("\nTesting MongoDB connection...")
        
        connect(
            host=mongodb_uri,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000
        )
        print("✓ Successfully connected to MongoDB Atlas!")
        disconnect()
        return True
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False

if __name__ == '__main__':
    setup_mongodb_atlas()
    
    confirm = input("\nWould you like to test the connection? (y/n): ").strip().lower()
    if confirm == 'y':
        test_connection()
