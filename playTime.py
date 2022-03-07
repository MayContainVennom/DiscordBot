import os
import random
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen


def search(list, player):
        for i in range(len(list)):
                if list[i][0] == player:
                        return True
        return False

def getPlayers():
    playerTab = []
    data = urlopen("").read()
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
        return playerLive

loop = True
playerCache = getPlayers()
while loop:
        time.sleep(60)
        playerLive = getPlayers()
        checkTable(playerCache,playerLive)
        playerCache = playerLive

