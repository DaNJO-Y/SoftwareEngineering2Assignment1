from App.models import Competition
from App.database import db

def create_competition(name, numberOfChallenges, location):
    newCompetition = Competition(name=name, numberOfChallenges=numberOfChallenges, location=location)
    db.session.add(newCompetition)
    db.session.commit()
    return newCompetition

def get_competition(id):
    return Competition.query.get(id)

def get_all_competitions():
    return Competition.query.all()

