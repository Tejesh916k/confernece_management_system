from bson import ObjectId

class Payment:
    def __init__(self, data):
        self.id = str(data.get('_id', ''))
        self.user_id = str(data.get('user_id', ''))
        self.amount = float(data.get('amount', 0))
        self.status = data.get('status', 'Pending')
        self.txn_id = data.get('txn_id', None)
    
    def to_dict(self):
        return {
            '_id': ObjectId(self.id),
            'user_id': self.user_id,
            'amount': self.amount,
            'status': self.status,
            'txn_id': self.txn_id
        }
