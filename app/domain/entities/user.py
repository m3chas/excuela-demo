from datetime import datetime

class User:
    def __init__(self, id=None, username='', password_hash='', email='', created_at=None):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.created_at = created_at or datetime.utcnow()
