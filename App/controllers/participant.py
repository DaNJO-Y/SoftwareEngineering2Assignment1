from App.models import Participant
from App.database import db

def create_participant(firstName, lastName, username, level):
    newParticipant = Participant(firstName, lastName, username, level=level)
    db.session.add(newParticipant)
    db.session.commit()
    return newParticipant

def get_participant_by_name(username):
    return Participant.query.filter_by(username=username).first()

def get_participant(id):
    return Participant.query.get(id)

def get_all_participants():
    return Participant.query.all()

def update_participant(id, username):
    participant = get_participant(id)
    if participant:
        participant.username = username
        db.session.add(participant)
        return db.session.commit()
    return None