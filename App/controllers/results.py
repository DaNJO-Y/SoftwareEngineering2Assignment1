from App.models import Results
from App.database import db

def create_results(competition_id, participant_id, challengesPassed, score, timeInMin, timeInSecs, rank):
    newResult = Results(competition_id=competition_id, participant_id=participant_id, challengesPassed=challengesPassed, score=score, timeInMin=timeInMin, timeInSecs=timeInSecs, rank=rank)
    db.session.add(newResult)
    db.session.commit()
    return newResult

def get_results_by_competition(competition_id):
    return Results.query.filter_by(competition_id=competition_id).all()

def get_results_by_participant(participant_id):
    return Results.query.filter_by(participant_id=participant_id).all()

def get_all_results():
    return Results.query.all()
