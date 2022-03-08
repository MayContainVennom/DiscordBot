import os
import random
import time
import sqlite3
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen


def sql_connection(db_file):
	con = None
	try:
		con = sqlite3.connect(db_file)
	except sqlite3.Error as e:
		print(e)
	return con

def sql_insert(conn, inputList):
	sql = ''' INSERT INTO playtable(user,uptime,timestamp)
		  VALUES(?,?,?) '''
	cur = conn.cursor()
	cur.execute(sql, inputList)
	conn.commit()
	return cur.lastrowid

def sql_main(user,uptime,timestamp):
	database = "playtime.db"
	# create  database connection
	conn = sql_connection(database)
	with conn:
		entryList = (user,uptime,timestamp)
		entry_id = sql_insert(conn, entryList)
		print(entry_id)

def search(list, player):
	for i in range(len(list)):
		if list[i][0] == player:
			return True
	return False

def getPlayers():
    playerTab = []
    data = urlopen("http://10.0.20.3:8080/feed/dedicated-server-stats.xml?code=a51fce89c74b87cfbe526cbbc5ab18eb").read()
    bs_data = BeautifulSoup(data, "xml")
    playerList = bs_data.find_all('Player')
    for i in playerList:
       cPlayer = i.get_text()
       uTime = i.get('uptime')
       if cPlayer:
           playerTab.append([cPlayer,uTime])
    return(playerTab)

def checkTable(playerCache,playerLive):
	for player, uptime in  playerCache:
		if search(playerLive, player):
			print(f'Player {player} is still online')
		else:
			print(f'Player {player} left, last playtime {uptime}')
			dateTimeObj = datetime.now()
			timeStamp = dateTimeObj.strftime("%d-%b-%Y (%H:%M)")
			sql_main(player,uptime,timeStamp)
	return playerLive

loop = True
playerCache = getPlayers()
while loop:
	time.sleep(60)
	playerLive = getPlayers()
	checkTable(playerCache,playerLive)
	playerCache = playerLive


