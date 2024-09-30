# Project Description
Competitions Platform

An application for students to showcase their participation in coding competitions.


* Create Competition

* Import competition results from file

* View competitions list

* View competition results

# Flask Commands

To initialize the database the initialize command is utilized.
```python
#inside wsgi.py

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')
```
The flask cli command goes as follows

```bash
$ flask init
```
# Participant Group
A Participant group was created to group all commands associated with participants. The following section highlights the commands of this group.

To list all comands associated with the participant group:
```bash
$ flask participant --help
```

To create a paricipant:
```python
#inside wsgi.py

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

app.cli.add_command(participant_cli) # add the group to the cli

```

The flask cli command goes as follows 
```bash
$  flask participant create Nora Beady Beadle Advanced
```

To list all participants
```python
#inside wsgi.py

participant_cli = AppGroup('participant', help='Participant object commands')

@participant_cli.command("list", help="List all participants")
def get_participants():
    participants = get_all_participants()
    print(participants)
app.cli.add_command(participant_cli) # add the group to the cli
```
The command line goes as follows
```bash
$ flask participant list
```

To find a participant by their username:
```python
#inside wsgi.py

participant_cli = AppGroup('participant', help='Participant object commands')

@participant_cli.command("find")
@click.argument('username',default='bob')
def get_participant(username):
    participant = get_participant_by_name(username)
    if not participant:
        print(f'{username} not found')
        return
    print(participant)

app.cli.add_command(participant_cli) # add the group to the cli
```
The command line goes as follows
```bash
$ flask participant find Beadle
```

To add a competition to a participant's competitions: 
```python
#inside wsgi.py

participant_cli = AppGroup('participant', help='Participant object commands')

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

app.cli.add_command(participant_cli) # add the group to the cli
```
The command line goes as follows
```bash
$ flask participant add Beadle Soft-Wear 15 London
```

To list a participant's competitions by username: 
```python
#inside wsgi.py

participant_cli = AppGroup('participant', help='Participant object commands')

@participant_cli.command("my-competitions", help="List a participant's competitions")
@click.argument('username', default='bob')
def get_participant_competitions(username):
    participant = get_participant_by_name(username)
    if not participant:
        print(f'{username} not found')
        return
    print(participant.competitions)

app.cli.add_command(participant_cli) # add the group to the cli
```
The command line goes as follows
```bash
$ flask participant my-competitions Beadle
```
# Command Group

A Competitions group was created to group all commands associated with competitions. The following section highlights the commands of this group.

To list all commands associated with the competitions group:
```bash
$ flask competition --help
```

To create a competition:
```python

competition_cli = AppGroup('competition', help='Competition object commands')

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

app.cli.add_command(competition_cli)
```

The command line goes as follows:
```bash
$ flask competition create Software-OverLoad 15 Toco,France
```

To list all competitions in table form:
```python
competition_cli = AppGroup('competition', help='Competition object commands')

@competition_cli.command("list" , help="List all created competitions in table form")
def list_competitions():
    comps = []
    allComps = get_all_competitions()
    for comp in allComps:
        comps.append([comp.id, comp.name, comp.numberOfChallenges, comp.location])
    print(tabulate(comps, headers=["ID", "Name", "Number Of Challenges", "Location"]))

app.cli.add_command(competition_cli)

```

The command line goes as follows:
```bash
$ flask competition list
```

To import results from a csv file for a competition:
```python
competition_cli = AppGroup('competition', help='Competition object commands')

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

```

The command line goes as follows:
```bash
$ flask competition import results2.csv
```

# Results Group

A Results group was created to group all commands associated with results. The following section highlights the commands of this group.

To list all commands associated with the results group:
```bash
$ flask result --help
```

To list the results for a given competition in table form:

```python
results_cli = AppGroup('result', help='Results object commands')

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

app.cli.add_command(results_cli)
```

The command line goes a follows:
```bash
$ flask result list-comp-results 2
```

To list all results of a given participant in table form:

```python
results_cli = AppGroup('result', help='Results object commands')

@results_cli.command("list-participant-results", help="list results by participants")
@click.argument('participant_id', default=1)
def list_participant_results(participant_id):
    results = []
    participantRes = get_results_by_participant(participant_id)
    for result in participantRes:
        results.append([result.rank, result.competition_id, result.challengesPassed, result.score, result.timeInMin, result.timeInSecs ])
    print(f'Results for  Participant {participant_id} : ')
    print(tabulate(results, headers=["Rank", "Competition Id", "Challenges Passed", "Score", "Time In Minuites", "Time In Seconds"]))
    
app.cli.add_command(results_cli)
```

To list all imported results in table form:

```python
results_cli = AppGroup('result', help='Results object commands')

@results_cli.command("list", help="list every result for every competition")
def list_results():
    results = []
    compResults = get_all_results()
    for result in compResults:
        results.append([result.rank, result.participant_id, result.challengesPassed, result.score, result.timeInMin, result.timeInSecs, result.competition_id ])
    print(tabulate(results, headers=["Rank", "Participant Id", "Challenges Passed", "Score", "Time In Minuites", "Time In Seconds", "Competition Id"]))
    
app.cli.add_command(results_cli)
```

The command line goes a follows:
```bash
$ flask result list
```








