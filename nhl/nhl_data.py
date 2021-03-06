import requests
import lxml.html
from pprint import pprint
from sys import exit
import json
import csv
from . import current_date
from datetime import datetime
from apscheduler.scheduler import Scheduler

# Start the scheduler
sched = Scheduler()
sched.start()

year = current_date.get_year()
month = current_date.get_month()
day = current_date.get_day()

def update_time():
    global year
    year = current_date.get_year()
    global month
    month = current_date.get_month()
    global day
    day = current_date.get_day()

sched.add_interval_job(update_time, hours=6)

teams_dictionary = {
 'devils': '01',
 'islanders': '02',
 'rangers': '03',
 'flyers': '04',
 'penguins': '05',
 'bruins': '06',
 'sabres': '07',
 'habs': '08',
 'sens': '09',
 'leafs': '10',
 #11 is not an active team
 'hurricanes': '12',
 'panthers': '13',
 'lightning': '14',
 'capitals': '15',
 'blackhawks': '16',
 'redwings': '17',
 'predators': '18',
 'blues': '19',
 'flames': '20',
 'avs': '21',
 'oilers': '22',
 'nucks': '23',
 'ducks': '24',
 'stars': '25',
 'kings': '26',
 'coyotes': '27',
 'sharks': '28',
 'bluejackets': '29',
 'wild': '30',
 #bunch of non active teams
 'knights': '54'
}

players = 'http://www.nhl.com/stats/rest/grouped/skaters/basic/season/skatersummary?cayenneExp=gameTypeId=%223%22%20and%20seasonId%3E=20142015%20and%20seasonId%3C=20162017&factCayenneExp=gamesPlayed%3E=1&sort=[{%22property%22:%22points%22,%22direction%22:%22DESC%22},{%22property%22:%22goals%22,%22direction%22:%22DESC%22},{%22property%22:%22assists%22,%22direction%22:%22DESC%22}]'
goalies = 'http://www.nhl.com/stats/rest/grouped/goalies/goalie_basic/season/goaliesummary?cayenneExp=gameTypeId=%222%22%20and%20playerPositionCode=%22G%22%20and%20seasonId%3E=20162017%20and%20seasonId%3C=20162017&factCayenneExp=gamesPlayed%3E=1&sort=[{%22property%22:%22wins%22,%22direction%22:%22DESC%22}]'


respPlayers = requests.get(players).text
respPlayers = json.loads(respPlayers)

respGoalies = requests.get(goalies).text
respGoalies = json.loads(respGoalies)

def get_mugshot(player_name):

	for x in range(0, len(respPlayers['data'])):
		if respPlayers['data'][x]['playerLastName'].lower() == player_name:
			return('https://nhl.bamcontent.com/images/headshots/current/168x168/' + str(respPlayers['data'][x]['playerId']) + '.jpg')

	for x in range(0, len(respGoalies['data'])):
		if respGoalies['data'][x]['playerLastName'].lower() == player_name:
			return('https://nhl.bamcontent.com/images/headshots/current/168x168/' + str(respGoalies['data'][x]['playerId']) + '.jpg')

def get_todays_game_from(team_name):
	date_string = year + '-' + '09' + '-' + '30'
	URL = 'https://statsapi.web.nhl.com/api/v1/schedule?startDate='+date_string+'&site=en_nhl&teamId='+teams_dictionary[team_name]
	resp = requests.get(URL).text
	return json.loads(resp)['dates'][0]['games'][0]

def get_linescore_from(team_name):
    date_string = year + '-' + '09' + '-' + '30'
    URL = 'https://statsapi.web.nhl.com/api/v1/schedule?startDate='+date_string+'&expand=schedule.linescore&site=en_nhl&teamId='+teams_dictionary[team_name]
    resp = requests.get(URL).text;
    return json.loads(resp)['dates'][0]['games'][0]['linescore']
