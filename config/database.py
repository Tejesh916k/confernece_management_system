import os
from mongoengine import connect, disconnect

_connection = None

class MongoDBConfig:
    """MongoDB Atlas Configuration"""
    MONGODB_URI = os.getenv('MONGODB_URI')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'conference_db')
    
    # Connection options for Atlas
    CONNECT_OPTIONS = {
        'serverSelectionTimeoutMS': 5000,
        'connectTimeoutMS': 10000,
        'retryWrites': True,
    }

def init_db(app):
    """Initialize MongoDB Atlas connection"""
    global _connection
    
    try:
        mongodb_uri = MongoDBConfig.MONGODB_URI
        
        if not mongodb_uri:
            raise ValueError('MONGODB_URI not found in .env file')
        
        if not mongodb_uri.startswith('mongodb+srv://'):
            raise ValueError('Invalid MONGODB_URI format')
        
        if '<db_password>' in mongodb_uri or '<password>' in mongodb_uri:
            raise ValueError('MONGODB_URI contains placeholder')
        
        # Disconnect any existing connections first
        try:
            disconnect('default')
        except:
            pass
        
        # Connect to MongoDB Atlas
        _connection = connect(
            db=MongoDBConfig.DATABASE_NAME,
            host=mongodb_uri,
            alias='default',
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000,
            retryWrites=True,
            w='majority'
        )
        
        print(f'[OK] Connected to MongoDB Atlas')
        print(f'[OK] Database: {MongoDBConfig.DATABASE_NAME}')
        
        return _connection
        
    except Exception as e:
        print(f'[ERROR] MongoDB connection error: {e}')
        raise

def close_db():
    """Close MongoDB connection"""
    try:
        disconnect('default')
        print('[OK] MongoDB connection closed')
    except Exception as e:
        print(f'[ERROR] Error closing MongoDB: {e}')
