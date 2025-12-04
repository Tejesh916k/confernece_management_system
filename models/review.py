from bson import ObjectId

class Review:
    def __init__(self, data):
        self.id = str(data.get('_id', ''))
        self.paper_id = str(data.get('paper_id', ''))
        self.reviewer_id = str(data.get('reviewer_id', ''))
        self.comments = data.get('comments', '')
        self.decision = data.get('decision', '')
    
    def to_dict(self):
        return {
            '_id': ObjectId(self.id),
            'paper_id': self.paper_id,
            'reviewer_id': self.reviewer_id,
            'comments': self.comments,
            'decision': self.decision
        }
