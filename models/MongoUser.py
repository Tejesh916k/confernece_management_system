from mongoengine import Document, StringField, EmailField, DateTimeField, BooleanField
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class MongoUser(Document):
    """MongoDB User Model for Authentication"""
    
    id = StringField(primary_key=True, required=True)
    username = StringField(required=True, unique=True, min_length=3, max_length=50)
    email = EmailField(required=True, unique=True)
    password_hash = StringField(required=True)
    full_name = StringField(required=True, max_length=100)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    last_login = DateTimeField()
    
    meta = {
        'collection': 'users',
        'db_alias': 'default',
        'indexes': [
            'username',
            'email',
            ('username', 'email')
        ],
        'strict': False
    }
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
