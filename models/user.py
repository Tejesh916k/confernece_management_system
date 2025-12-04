from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])  # This must be string and is required by Flask-Login!
        self.email = user_data['email']
        self.role = user_data.get('role', 'User')
