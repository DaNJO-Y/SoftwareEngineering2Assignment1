from App.database import db

class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey('participant.id'),nullable=True)
    name = db.Column(db.String(50), nullable=False)
    numberOfChallenges = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    

    def __init__(self, name, numberOfChallenges, location):

        self.name = name
        self.numberOfChallenges = numberOfChallenges
        self.location = location
        
    def __repr__(self):
        return f'<Competition - Name = {self.name} | {self.id} | {self.location} | Number of Challenges {self.numberOfChallenges}>'

    

    
