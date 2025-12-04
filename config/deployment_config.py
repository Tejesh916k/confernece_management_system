"""
Deployment Configuration for Various Platforms
"""

import os

class DeploymentConfig:
    """Configuration for different deployment platforms"""
    
    # Environment detection
    ENVIRONMENT = os.getenv('FLASK_ENV', 'development')
    IS_PRODUCTION = ENVIRONMENT == 'production'
    
    # Database
    MONGODB_URI = os.getenv('MONGODB_URI')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'conference_db')
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    
    # Server
    HOST = os.getenv('HOST', '0.0.0.0' if IS_PRODUCTION else 'localhost')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = not IS_PRODUCTION
    
    @staticmethod
    def validate_config():
        """Validate that all required configs are present"""
        required = ['MONGODB_URI']
        missing = [key for key in required if not os.getenv(key)]
        
        if missing:
            raise ValueError(f"Missing required environment variables: {missing}")
        
        return True


# Platform-specific configurations
class HerokuConfig(DeploymentConfig):
    """Heroku deployment configuration"""
    PROPAGATE_EXCEPTIONS = True


class RailwayConfig(DeploymentConfig):
    """Railway deployment configuration"""
    PROPAGATE_EXCEPTIONS = True


class RenderConfig(DeploymentConfig):
    """Render deployment configuration"""
    PROPAGATE_EXCEPTIONS = True


class PythonAnywhereConfig(DeploymentConfig):
    """PythonAnywhere deployment configuration"""
    PROPAGATE_EXCEPTIONS = True


class AwsConfig(DeploymentConfig):
    """AWS deployment configuration"""
    PROPAGATE_EXCEPTIONS = True
