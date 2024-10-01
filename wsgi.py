import click, pytest, sys, csv
from tabulate import tabulate
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, Participant
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize, create_participant, get_all_participants, get_participant_by_name, create_competition, get_competition, get_all_competitions,create_results, get_results_by_competition, get_results_by_participant, get_all_results )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

participant_cli = AppGroup('participant', help='Participant object commands')

# This function creates a participant
@participant_cli.command("create", help="Creates a participant")
@click.argument('firstname',default='jack')
@click.argument('lastname',default='greg')
@click.argument('username',default='jeg')
@click.argument('level',default='Beginner')
def createParticipant(firstname, lastname, username, level):
    new_participant = create_participant(firstname, lastname, username, level)
    try:
        db.session.add(new_participant)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        print(e.orig)
        print("Username already taken!")
    else:
        print("Participant created")
        print(new_participant)

# This function lists all participants that are created
@participant_cli.command("list", help="List all participants")
def get_participants():
    participants = get_all_participants()
    print(participants)

# This function finds and retrieves a participant based on a username passed as an argument
@participant_cli.command("find")
@click.argument('username',default='bob')
def get_participant(username):
    participant = get_participant_by_name(username)
    if not participant:
        print(f'{username} not found')
        return
    print(participant)

# This function creates a competition and adds it to the participant's list of competitions
@participant_cli.command('add', help="Associates a created competition with a participant")
@click.argument('username', default="bob")
@click.argument('name',default='Software-Comp')
@click.argument('numberofchallenges', default=15)
@click.argument('location', default='San-Francisco')
def add_comp(username, name, numberofchallenges, location):
    participant = get_participant_by_name(username)
    if not participant:
        print(f'{username} not found')
        return
    new_comp = create_competition(name, numberofchallenges, location)
    participant.competitions.append(new_comp)
    db.session.add(participant)
    db.session.commit()
    print('Competition added')

# This function retrieves and lists all the competitions present in a participant's list of competitions
@participant_cli.command("my-competitions", help="List a participant's competitions")
@click.argument('username', default='bob')
def get_participant_competitions(username):
    participant = get_participant_by_name(username)
    if not participant:
        print(f'{username} not found')
        return
    print(participant.competitions)

app.cli.add_command(participant_cli) # add the group to the cli

competition_cli = AppGroup('competition', help='Competition object commands')

# This function creates a competition
@competition_cli.command("create", help="Create a competition")
@click.argument('name',default='Software-Comp')
@click.argument('numberofchallenges', default=15)
@click.argument('location', default='San-Francisco')
def create_comp(name, numberofchallenges, location):
    new_competition = create_competition(name, numberofchallenges, location)
    try:
        db.session.add(new_competition)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        print(e.orig)
        print("No funding for Competition")
    else:
        print(new_competition)

        
# This function retrtieves and lists all create competitions in table form
@competition_cli.command("list" , help="List all created competitions in table form")
def list_competitions():
    comps = []
    allComps = get_all_competitions()
    for comp in allComps:
        comps.append([comp.id, comp.name, comp.numberOfChallenges, comp.location])
    print(tabulate(comps, headers=["ID", "Name", "Number Of Challenges", "Location"]))

# This function imports a csv file containing results for a specific competition
@competition_cli.command("import", help="import results from a csv file for a competition")
@click.argument('name')
def import_file(name):
    with open(f'{name}') as file:
        reader = csv.DictReader(file) 
        for row in reader:
            new_result = create_results(int(row['competition_id']), int(row['participant_id']), int(row['challengesPassed']), int(row['score']), int(row['timeInMin']), int(row['timeInSecs']), int(row['rank'])) 
            db.session.add(new_result)
        db.session.commit()
        print('results imported')

app.cli.add_command(competition_cli)

results_cli = AppGroup('result', help='Results object commands')

# This function retrieves and list all results for a given competition
@results_cli.command("list-comp-results", help="list results by competition")
@click.argument('competition_id', default= 1)
def list_competition_results(competition_id):
    results = []
    competition = get_competition(competition_id)
    if not competition:
        print(f'There is no Competition with id: {competition_id}')
        return
    compResults = get_results_by_competition(competition_id)
    for result in compResults:
        results.append([result.rank, result.participant_id, result.challengesPassed, result.score, result.timeInMin, result.timeInSecs ])
    print(f'Results for {competition.name} : ')
    print(tabulate(results, headers=["Rank", "Participant Id", "Challenges Passed", "Score", "Time In Minuites", "Time In Seconds"]))

# This function retrieves and lists all results for a given participant over all competitions
@results_cli.command("list-participant-results", help="list results by participants")
@click.argument('participant_id', default=1)
def list_participant_results(participant_id):
    results = []
    participantRes = get_results_by_participant(participant_id)
    for result in participantRes:
        results.append([result.rank, result.competition_id, result.challengesPassed, result.score, result.timeInMin, result.timeInSecs ])
    print(f'Results for  Participant {participant_id} : ')
    print(tabulate(results, headers=["Rank", "Competition Id", "Challenges Passed", "Score", "Time In Minuites", "Time In Seconds"]))
    
# This function retrieves and lists all results
@results_cli.command("list", help="list every result for every competition")
def list_results():
    results = []
    compResults = get_all_results()
    for result in compResults:
        results.append([result.rank, result.participant_id, result.challengesPassed, result.score, result.timeInMin, result.timeInSecs, result.competition_id ])
    print(tabulate(results, headers=["Rank", "Participant Id", "Challenges Passed", "Score", "Time In Minuites", "Time In Seconds", "Competition Id"]))

app.cli.add_command(results_cli)

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)