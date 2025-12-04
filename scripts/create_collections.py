"""
Create MongoDB Collections for Conference Management System
Run this after creating the database
"""

from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def create_collections():
    """Create all required collections"""
    
    # Connect to MongoDB
    client = MongoClient(os.getenv('MONGODB_URI'))
    db = client['conference_db']
    
    collections_to_create = [
        'conferences',
        'sessions',
        'attendees',
        'registrations',
        'papers',
    ]
    
    print("Creating collections...\n")
    
    for collection_name in collections_to_create:
        try:
            # Create collection
            db.create_collection(collection_name)
            print(f"✓ Created collection: {collection_name}")
        except Exception as e:
            if 'already exists' in str(e):
                print(f"ℹ Collection already exists: {collection_name}")
            else:
                print(f"✗ Error creating {collection_name}: {e}")
    
    # Create indexes for better performance
    print("\nCreating indexes...\n")
    
    # Conferences index
    db.conferences.create_index('name')
    db.conferences.create_index('start_date')
    print("✓ Created indexes for conferences")
    
    # Sessions index
    db.sessions.create_index('title')
    db.sessions.create_index('conference_id')
    db.sessions.create_index('speaker')
    print("✓ Created indexes for sessions")
    
    # Attendees index
    db.attendees.create_index('email', unique=True)
    db.attendees.create_index('name')
    print("✓ Created indexes for attendees")
    
    # Registrations index
    db.registrations.create_index([('attendee_id', 1), ('session_id', 1)])
    print("✓ Created indexes for registrations")
    
    print("\n✓ All collections and indexes created successfully!")
    
    # Close connection
    client.close()

if __name__ == '__main__':
    create_collections()
