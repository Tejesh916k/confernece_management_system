from bson import ObjectId

class Paper:
    def __init__(self, data):
        self.id = str(data.get('_id', ''))
        self.user_id = str(data.get('user_id', ''))
        self.filename = data.get('filename', '')
        self.filepath = data.get('filepath', '')
        self.status = data.get('status', 'Pending')
        self.reviewer_id = str(data.get('reviewer_id', '')) if data.get('reviewer_id') else None
        self.title = data.get('title', '')
        self.abstract = data.get('abstract', '')
    
    def to_dict(self):
        return {
            '_id': ObjectId(self.id),
            'user_id': self.user_id,
            'filename': self.filename,
            'filepath': self.filepath,
            'status': self.status,
            'reviewer_id': self.reviewer_id,
            'title': self.title,
            'abstract': self.abstract
        }
