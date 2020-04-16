import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wad2_team_project.settings')

import django
django.setup()
from rowassist.models import Club, Athlete, Session, SessionInterval, SessionEntry
from django.contrib.auth.models import User
import manage

def populate():

	clubs = [
		{"name": "Glasgow University Boat Club", "short":"GUBC"},
		{"name": "Strathclyde University Boat Club", "short":"SUBC"},
		{"name": "Edinburgh University Boat Club", "short":"EUBC"},
		{"name": "Aberdeen University Boat Club", "short":"AUBC"},
		{"name": "Glasgow Rowing Club", "short":"GRC"},
		{"name": "Clydesdale ARC", "short":"CARC"},
		{"name": "George Heriot's School Rowing Club", "short":"GHSRC"}
	]

	users = [
		#GUBC Coaches
		{"username": "PaddyHudson",
		"password": "123abc",
		"email": "PaddyHudson@gmail.com",
		"first_name": "Paddy",
		"last_name": "Hudson",
		"is_coach": True,
		"club": "GUBC",
		"requested_club": None},

		{"username": "IainDocwra",
		"password": "123abc",
		"email": "IainDocwra@gmail.com",
		"first_name": "Iain",
		"last_name": "Docwra",
		"is_coach": True,
		"club": "GUBC",
		"requested_club": None},

		{"username": "FraserQuinn",
		"password": "123abc",
		"email": "FraserQuinn@gmail.com",
		"first_name": "Fraser",
		"last_name": "Quinn",
		"is_coach": True,
		"club": "GUBC",
		"requested_club": None},

		#GUBC Athletes
		{"username": "RoryYoung",
		"password": "123abc",
		"email": "RoryYoung@gmail.com",
		"first_name": "Rory",
		"last_name": "Young",
		"is_coach": False,
		"club": "GUBC",
		"requested_club": None},

		{"username": "MattJackson",
		"password": "123abc",
		"email": "MattJackson@gmail.com",
		"first_name": "Matt",
		"last_name": "Jackson",
		"is_coach": False,
		"club": "GUBC",
		"requested_club": None},

		{"username": "CalumYoung",
		"password": "123abc",
		"email": "CalumYoung@gmail.com",
		"first_name": "Calum",
		"last_name": "Young",
		"is_coach": False,
		"club": "GUBC",
		"requested_club": None},

		{"username": "SeumasBrett",
		"password": "123abc",
		"email": "SeumasBrett@gmail.com",
		"first_name": "Seumas",
		"last_name": "Brett",
		"is_coach": False,
		"club": "GUBC",
		"requested_club": None},

		{"username": "RoryCartlidge",
		"password": "123abc",
		"email": "RoryCartlidge@gmail.com",
		"first_name": "Rory",
		"last_name": "Cartlidge",
		"is_coach": False,
		"club": "GUBC",
		"requested_club": None},
	]

	sessions = [
		{"club":"GUBC",
		"type": "S",
		"date": "2019-03-14",
		"description": "Optional Erg/sliders 50' steady R:20-22",
		"name": "50'Erg",
		"distance": None,
		"time": "00:50:00",
		"rate": 20,
		"rest": None,
		"intervalNo": None,
		"isActive": False},

		{"club":"GUBC",
		"type": "F",
		"date": "2019-03-22",
		"description": "Erg 3 x 25' R:20 2' rest (steady - max effort split, +2)",
		"name": "3 x 25'",
		"distance": None,
		"time": "00:25:00",
		"rate": 20,
		"rest": "00:02:00",
		"intervalNo": 3,
		"isActive": False},

		{"club":"GUBC",
		"type": "F",
		"date": "2019-03-20",
		"description": "3k warm-up + 8 x 5' R:22-26 3-4' rest + 2-3k paddle",
		"name": "8 x 5'",
		"distance": None,
		"time": "00:05:00",
		"rate": 26,
		"rest": "00:04:00",
		"intervalNo": 8,
		"isActive": True},

		{"club":"GUBC",
		"type": "F",
		"date": "2019-03-22",
		"description": "Erg 3 x 7' 3', 2', 1', 1' R:26+ 8' rest full squad",
		"name": "3 x 7'",
		"distance": None,
		"time": "00:07:00",
		"rate": 26,
		"rest": "00:04:00",
		"intervalNo": 3,
		"isActive": True},

		{"club":"GUBC",
		"type": "S",
		"date": "2019-03-23",
		"description": "2k test, max effort",
		"name": "2k",
		"distance": 2000,
		"time": None,
		"rate": 36,
		"rest": None,
		"intervalNo": None,
		"isActive": True},

		{"club":"GUBC",
		"type": "V",
		"date": "2019-03-24",
		"description": "15', 20', 25' 30'",
		"name": "15', 20', 25' 30'",
		"distance": None,
		"time": "01:30:00",
		"rate": None,
		"rest": None,
		"intervalNo": None,
		"isActive": True},
	]

	sessionIntervals = [
		{"session": "15', 20', 25' 30'",
		"intervalNo": 0,
		"distance": None,
		"time": "00:15:00",
		"rate": 20,
		"rest": "00:02:00"},

		{"session": "15', 20', 25' 30'",
		"intervalNo": 1,
		"distance": None,
		"time": "00:20:00",
		"rate": 20,
		"rest": "00:02:00"},

		{"session": "15', 20', 25' 30'",
		"intervalNo": 2,
		"distance": None,
		"time": "00:25:00",
		"rate": 20,
		"rest": "00:02:00"},

		{"session": "15', 20', 25' 30'",
		"intervalNo": 3,
		"distance": None,
		"time": "00:30:00",
		"rate": 20,
		"rest": "00:02:00"},
	]

	session_entries = []
	'''
	session_entries = [
		{"athlete": 'RoryYoung',
		 "session": '2k'},

		{"athlete": 'RoryYoung',
		 "session": "3 x 7'"},

		{"athlete": 'RoryYoung',
		 "session": "3 x 25'"},

		{"athlete": 'RoryYoung',
		 "session": "50'Erg"},

		{"athlete": 'MattJackson',
		 "session": '2k'},

		{"athlete": 'MattJackson',
		 "session": "3 x 7'"},

		{"athlete": 'MattJackson',
		 "session": "3 x 25'"},

		{"athlete": 'MattJackson',
		 "session": "50'Erg"},

		{"athlete": 'SeumasBrett',
		 "session": '2k'},

		{"athlete": 'SeumasBrett',
		 "session": "3 x 7'"},

		{"athlete": 'SeumasBrett',
		 "session": "3 x 25'"},

		{"athlete": 'SeumasBrett',
		 "session": "50'Erg"},
	]'''

	print("---Adding Clubs---")
	for club in clubs:
		add_club(club)
		print(club["name"])

	print("")
	print ("---Adding Users---")
	for user in users:
		add_user(user)
		print(user['username'])

	print("")
	print("---Adding Sessions---")
	for session in sessions:
		add_session(session)
		print(session['name'])

	print("")
	print("---Adding Session Intervals")
	for interval in sessionIntervals:
		add_interval(interval)
		print(interval['session'] + ", " + str(interval['intervalNo']))

	print("")
	print("---Adding Session Entries---")
	for session_entry in session_entries:
		add_session_entry(session_entry)
		print(session_entry['athlete'])


def add_club(club):
	club = Club.objects.get_or_create(name=club["name"], short_name=club["short"])


def add_user(d):
	user = User.objects.get_or_create(username=d['username'], email=d['email'], first_name=d['first_name'], last_name=d['last_name'])
	user[0].set_password(d['password'])
	user[0].save()

	if d['club'] is None:
		club = None
	else:
		club = Club.objects.get(short_name=d['club'])

	if d['requested_club'] is None:
		requested_club = None
	else:
		requested_club = Club.objects.get(short_name=d['requested_club'])

	athlete = Athlete.objects.get_or_create(user=user[0], is_coach=d['is_coach'], club=club, requested_club=requested_club)

def add_session(d):
	club = Club.objects.get(short_name=d['club'])

	session = Session.objects.get_or_create(club=club, type=d['type'], date=d['date'], description=d['description'], name=d['name'], distance=d['distance'], time=d['time'], rate=d['rate'], rest=d['rest'], intervalNo=d['intervalNo'], isActive=d['isActive'] )

def add_interval(d):
	session = Session.objects.get(name=d['session'])

	interval = SessionInterval.objects.get_or_create(session=session, intervalNo=d['intervalNo'], distance=d['distance'], time=d['time'], rate=d['rate'], rest=d['rest'])


def add_session_entry(d):
	user = User.objects.get(username=d['athlete'])
	athlete = user.athlete
	session = Session.objects.get(name=d['session'])

	session_entry = SessionEntry.objects.get_or_create(athlete=athlete, session=session)


if __name__ == '__main__':
	print("Starting Row Assist population script...")
	populate()