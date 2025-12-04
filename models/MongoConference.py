from mongoengine import Document, StringField, FloatField, DateTimeField, BooleanField, IntField, ListField
from datetime import datetime
import uuid

class MongoConference(Document):
    """MongoDB Conference Model"""
    
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    name = StringField(required=True, unique=True)
    description = StringField(required=True)
    field = StringField()  # Education field/category
    start_date = DateTimeField(required=True)
    end_date = DateTimeField(required=True)
    location = StringField(required=True)
    city = StringField()
    country = StringField()
    max_attendees = IntField(default=100)
    registration_fee = FloatField(default=0)
    status = StringField(default='upcoming', choices=['upcoming', 'ongoing', 'completed', 'cancelled'])
    organizer_id = StringField(required=True)
    logo = StringField()  # URL to logo
    banner = StringField()  # URL to banner image
    website = StringField()
    attendees = ListField(StringField(), default=[])
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'conferences',
        'db_alias': 'default',
        'indexes': ['name', 'start_date', 'organizer_id', 'status']
    }
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'location': self.location,
            'city': self.city,
            'country': self.country,
            'max_attendees': self.max_attendees,
            'registration_fee': self.registration_fee,
            'status': self.status,
            'organizer_id': self.organizer_id,
            'logo': self.logo,
            'banner': self.banner,
            'website': self.website,
            'attendee_count': len(self.attendees),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
