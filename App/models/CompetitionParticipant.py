from App.database import db

class CompetitionParticipant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey('participant.id'),nullable=False)
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'),nullable=False)
    

    