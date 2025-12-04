from mongoengine import Document, StringField, DateTimeField, IntField, ListField
from datetime import datetime

class MongoSession(Document):
    """MongoDB Session Model"""
    
    id = StringField(primary_key=True, required=True)
    title = StringField(required=True)
    description = StringField(required=True)
    speaker = StringField(required=True)
    start_time = DateTimeField(required=True)
    end_time = DateTimeField(required=True)
    location = StringField(required=True)
    capacity = IntField(required=True, min_value=1)
    attendees = ListField(StringField(), default=[])
    conference_id = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'sessions',
        'indexes': ['title', 'speaker', 'conference_id'],
        'db_alias': 'default'
    }
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'speaker': self.speaker,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'location': self.location,
            'capacity': self.capacity,
            'attendees': self.attendees,
            'available_seats': self.capacity - len(self.attendees),
            'conference_id': self.conference_id,
            'created_at': self.created_at.isoformat()
        }
