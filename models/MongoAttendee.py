from mongoengine import Document, StringField, EmailField, ListField, DateTimeField
from datetime import datetime

class MongoAttendee(Document):
    """MongoDB Attendee Model"""
    
    id = StringField(primary_key=True, required=True)
    name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    phone = StringField()
    company = StringField()
    registered_sessions = ListField(StringField(), default=[])
    registration_date = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'attendees',
        'indexes': ['email', 'name'],
        'db_alias': 'default'
    }
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'company': self.company,
            'registered_sessions': self.registered_sessions,
            'registration_date': self.registration_date.isoformat()
        }
