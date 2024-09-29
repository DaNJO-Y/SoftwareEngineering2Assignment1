import click, pytest, sys, csv
from tabulate import tabulate
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, Participant
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize, create_participant, get_all_participants, get_participant_by_name, create_competition, get_competition, get_all_competitions, get_results_by_competition, get_results_by_participant, get_all_results )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

@app.cli.command("create-participant")
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
        print(new_participant)

@app.cli.command('get-participants')
def get_participants():
    participants = get_all_participants()
    print(participants)

@app.cli.command('get-participant')
@click.argument('username',default='bob')
def get_participant(username):
    participant = get_participant_by_name(username)
    if not participant:
        print(f'{username} not found')
        return
    print(participant)

@app.cli.command('create-competition')
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

#added to participant
@app.cli.command('add-competition')
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

@app.cli.command('get-participant-competitions')
@click.argument('username', default='bob')
def get_participant_competitions(username):
    participant = get_participant_by_name(username)
    if not participant:
        print(f'{username} not found')
        return
    print(participant.competitions)


@app.cli.command('get-competitions')
def list_competitions():
    comps = []
    allComps = get_all_competitions()
    for comp in allComps:
        comps.append([comp.name, comp.numberOfChallenges, comp.location])
    print(tabulate(comps, headers=["Name", "Number Of Challenges", "Location"]))

@app.cli.command('get-competition-results')
@click.argument('competition_id', default= 1)
def list_competition_results(competition_id):
    results = []
    compResults = get_results_by_competition(competition_id)
    for result in compResults:
        results.append([result.rank, result.participant_id, result.challengesPassed, result.score, result.timeInMin, result.timeInSecs ])
    competition = get_competition(competition_id)
    print(f'Results for {competition.name} : ')
    print(tabulate(results, headers=["Rank", "Participant Id", "Challenges Passed", "Score", "Time In Minuites", "Time In Seconds"]))

@app.cli.command('get-participant-results')
@click.argument('participant_id', default=1)
def list_participant_results(participant_id):
    results = []
    participantRes = get_results_by_participant(participant_id)
    for result in participantRes:
        results.append([result.rank, result.competition_id, result.challengesPassed, result.score, result.timeInMin, result.timeInSecs ])
    print(f'Results for  Participant {participant_id} : ')
    print(tabulate(results, headers=["Rank", "Competition Id", "Challenges Passed", "Score", "Time In Minuites", "Time In Seconds"]))
    

@app.cli.command('get-results')
def list_results():
    results = []
    compResults = get_all_results()
    for result in compResults:
        results.append([result.rank, result.participant_id, result.challengesPassed, result.score, result.timeInMin, result.timeInSecs, result.competition_id ])
    print(tabulate(results, headers=["Rank", "Participant Id", "Challenges Passed", "Score", "Time In Minuites", "Time In Seconds", "Competition Id"]))


'''
User Commands
'''
#move all functions to groups
participant_cli = AppGroup('participant', help='Participant object commands')

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
        print(new_participant)

@participant_cli.command("list")
def get_participants():
    participants = get_all_participants()
    print(participants)

@participant_cli.command("find")
@click.argument('username',default='bob')
def get_participant(username):
    participant = get_participant_by_name(username)
    if not participant:
        print(f'{username} not found')
        return
    print(participant)

@participant_cli.command('add')
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

@participant_cli.command("my-competitions")
@click.argument('username', default='bob')
def get_participant_competitions(username):
    participant = get_participant_by_name(username)
    if not participant:
        print(f'{username} not found')
        return
    print(participant.competitions)

app.cli.add_command(participant_cli) # add the group to the cli


competition_cli = AppGroup('competition', help='Competition object commands')


app.cli.add_command(competition_cli)


results_cli = AppGroup('result', help='Results object commands')


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