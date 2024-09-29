import csv
from .user import create_user
from .participant import *
from .competition import *
from .results import *
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    bob = create_participant('bob', 'roberts', 'BoB', 'Beginner')
    sally = create_participant('sally', 'salvorn', 'Sal', 'Immediate')
    rick = create_participant('ricardo', 'richards', 'rickGamer', 'Advanced')
    competitionOne = create_competition('Software-Stars', 15, 'London-UK')
    db.session.add_all([bob, sally, rick, competitionOne])
    db.session.commit()

    with open('results.csv') as file:
        reader = csv.DictReader(file) 
        for row in reader:
            new_result = create_results(int(row['competition_id']), int(row['participant_id']), int(row['challengesPassed']), int(row['score']), int(row['timeInMin']), int(row['timeInSecs']), int(row['rank'])) 
            db.session.add(new_result)
        db.session.commit()
