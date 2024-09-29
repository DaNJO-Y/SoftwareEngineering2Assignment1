from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(20), nullable=False)
    lastName = db.Column(db.String(20), nullable=False)
    level = db.Column(db.String(50), nullable=False)
    competitions = db.relationship('Competition', backref='participant', lazy=True, cascade="all, delete-orphan")
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=True)

    def __init__(self, firstName, lastName, username, level):

        self.firstName = firstName
        self.lastName = lastName
        self.username = username
        self.level = level
        

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<Participant - Id - {self.id} | {self.firstName} | {self.lastName} | level - {self.level} | username - {self.username}>'

