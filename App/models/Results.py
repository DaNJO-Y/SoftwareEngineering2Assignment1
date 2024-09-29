from App.database import db

class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'),nullable=False)
    participant_id = db.Column(db.Integer, db.ForeignKey('participant.id'),nullable=False)
    challengesPassed = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    timeInMin = db.Column(db.Integer, nullable=False)
    timeInSecs = db.Column(db.Integer, nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    
    def __init__(self, competition_id, participant_id, challengesPassed, score, timeInMin, timeInSecs, rank):

        self.competition_id = competition_id
        self.participant_id = participant_id
        self.challengesPassed = challengesPassed
        self.score = score
        self.timeInMin = timeInMin
        self.timeInSecs = timeInSecs
        self.rank = rank

    def __repr__(self):
        return f'<Results {self.rank} - {self.participant_id} - {self.score} {self.challengesPassed} {self.timeInMin} : {self.timeInSecs}>'


