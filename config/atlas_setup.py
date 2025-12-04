"""
MongoDB Atlas Setup Configuration
Use this to configure your Atlas database for deployment
"""

import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

class AtlasSetup:
    """
    Step-by-step MongoDB Atlas Configuration
    """
    
    @staticmethod
    def generate_connection_string(username, password, cluster_url, database_name):
        """
        Generate MongoDB Atlas connection string
        
        Args:
            username: Database user (e.g., 'conference_user')
            password: Database password
            cluster_url: Cluster URL (e.g., 'cluster0.abc123.mongodb.net')
            database_name: Database name (e.g., 'conference_db')
        
        Returns:
            Formatted MongoDB Atlas connection string
        """
        # URL encode password to handle special characters
        encoded_password = quote_plus(password)
        
        connection_string = (
            f"mongodb+srv://{username}:{encoded_password}@{cluster_url}/"
            f"{database_name}?retryWrites=true&w=majority"
        )
        
        return connection_string
    
    @staticmethod
    def create_env_file(connection_string, database_name='conference_db'):
        """Create .env file with Atlas configuration"""
        env_content = f"""# MongoDB Atlas Configuration for Deployment
MONGODB_URI={connection_string}
DATABASE_NAME={database_name}

# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-production-secret-key-change-this

# Server Configuration
HOST=0.0.0.0
PORT=5000

# Atlas User Credentials (for reference)
# USERNAME=conference_user
# PASSWORD=your_password_here
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✓ .env file created for deployment")
        return True
    
    @staticmethod
    def print_setup_instructions():
        """Print step-by-step Atlas setup instructions"""
        instructions = """
╔════════════════════════════════════════════════════════════════════════╗
║          MongoDB Atlas Setup for Deployment (No Compass)              ║
╚════════════════════════════════════════════════════════════════════════╝

STEP 1: CREATE MONGODB ATLAS CLUSTER
─────────────────────────────────────
1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up or log in
3. Create a new project (e.g., "Conference Management")
4. Click "Build a Database"
5. Choose "M0 Shared" (Free tier)
6. Select your cloud provider (AWS recommended)
7. Choose region closest to your deployment server
8. Click "Create Deployment"
⏱️  Wait 5-10 minutes for cluster creation...


STEP 2: CREATE DATABASE USER
──────────────────────────────
1. Go to "Database Access" (left sidebar)
2. Click "Add New Database User"
3. Enter username: conference_user
4. Set strong password (save this somewhere safe!)
5. Select "Read and write to any database"
6. Click "Add User"


STEP 3: WHITELIST IP ADDRESSES
────────────────────────────────
1. Go to "Network Access" (left sidebar)
2. Click "Add IP Address"
3. For development: Add your machine IP
4. For deployment: Add your server/app IP
5. Or use 0.0.0.0/0 (allows all IPs - use only for testing)


STEP 4: GET CONNECTION STRING
──────────────────────────────
1. Go to "Databases" or "Clusters"
2. Click "Connect" on your cluster
3. Select "Drivers" → "Python"
4. Copy the connection string
5. Replace <password> with your database user password
6. Replace <myFirstDatabase> with 'conference_db'

Example format:
mongodb+srv://conference_user:password@cluster0.abc123.mongodb.net/conference_db?retryWrites=true&w=majority


STEP 5: CONFIGURE YOUR APPLICATION
───────────────────────────────────
1. Run this script to set up .env file
2. Update requirements.txt with dependencies
3. Deploy with your chosen platform


DEPLOYMENT PLATFORMS SUPPORTED:
────────────────────────────────
✓ Heroku
✓ Railway
✓ Render
✓ PythonAnywhere
✓ AWS
✓ Google Cloud
✓ Azure
✓ Your own server

"""
        print(instructions)


def interactive_setup():
    """Interactive setup for Atlas configuration"""
    print("\n" + "="*70)
    print("MongoDB Atlas Interactive Setup")
    print("="*70)
    
    AtlasSetup.print_setup_instructions()
    
    print("\nEnter your Atlas details:")
    print("-" * 70)
    
    username = input("Database username (e.g., conference_user): ").strip()
    password = input("Database password: ").strip()
    cluster_url = input("Cluster URL (e.g., cluster0.abc123.mongodb.net): ").strip()
    database_name = input("Database name (default: conference_db): ").strip() or "conference_db"
    
    if not all([username, password, cluster_url]):
        print("✗ Error: All fields are required")
        return False
    
    # Generate connection string
    connection_string = AtlasSetup.generate_connection_string(
        username, password, cluster_url, database_name
    )
    
    print("\n" + "="*70)
    print("Generated Connection String:")
    print("="*70)
    print(connection_string)
    print("="*70)
    
    # Create .env file
    confirm = input("\nCreate .env file with this configuration? (y/n): ").strip().lower()
    if confirm == 'y':
        AtlasSetup.create_env_file(connection_string, database_name)
        print("✓ Configuration saved to .env file")
        return True
    else:
        print("✗ Setup cancelled")
        return False


if __name__ == '__main__':
    interactive_setup()
