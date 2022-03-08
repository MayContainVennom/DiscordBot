import os
import random
import sqlite3
from bs4 import BeautifulSoup
from urllib.request import urlopen

import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext import tasks

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

PLAYER_CHANNEL = os.getenv('DISCORD_PLAYER_CHANNEL')
SERVER_XML = os.getenv('SERVER_XML')

client = commands.Bot(command_prefix=['!'])

def takeSecond(elem):
	return elem[1]

def sql_connection(db_file):
        con = None
        try:
                con = sqlite3.connect(db_file)
        except sqlite3.Error as e:
                print(e)
        return con

def create_sqlList():
        playerList = []
        playerUnique = []
        player_uptime = 0
        player_final = []
        database = "playtime.db"
        con = sql_connection(database)
        cur = con.cursor()
        cur.execute(" SELECT * FROM playtable;")
        rawList = cur.fetchall()
        con.close()
        # Creating a list of all the players
        for i in rawList:
                playerList.append(i[0])
        #taking duplicate entries out of the list
        playerUnique = list(dict.fromkeys(playerList))
        for i in playerUnique: 
                for player,uptime,time in rawList:
                        if player == i:
                                player_uptime = player_uptime + uptime
#               print(f'{i}s uptime is {player_uptime}')
                player_final.append([i,player_uptime])
                player_uptime = 0
        return player_final

def getOnline():
    data = urlopen("SERVER_XML").read()
    Bs_data = BeautifulSoup(data, "xml")
    b_unique = Bs_data.find('Slots')
    value = b_unique.get('numUsed')
    return(value)

def getPlayers():
    playerTab = []
    data = urlopen("SERVER_XML").read()
    bs_data = BeautifulSoup(data, "xml")
    playerList = bs_data.find_all('Player')
    for i in playerList:
       cPlayer = i.get_text()
       uTime = i.get('uptime')
       if cPlayer:
           playerTab.append([cPlayer,uTime])
    return(playerTab)

@client.listen()
async def on_ready():
    countChannel.start()
    embedOnline.start()
    embedLeaderboard.start()
    print(f'{client.user} is alive and listening for Discord events')


@tasks.loop(minutes=5)
async def countChannel():
    channel = client.get_channel(CHANNEL_ID)
    new_name = "✅Players Online {}/16✅".format(getOnline())
    print(new_name)
    await channel.edit(name=new_name)

@tasks.loop(minutes=2)
async def embedOnline():
	channel = client.get_channel(CHANNEL_ID)
	msg_id = MESSAGE_ID
	embedDisc = "Online Players {}/16".format(getOnline())
	embed=discord.Embed(title="Realistic Farming UK Server", description=embedDisc, color=0xff00d0)
	playersTab = getPlayers()
	playerField = "\n".join([f"{player} - {time} Mins" for player, time in playersTab])
	if playerField:
		embed.add_field(name="Players:",value=playerField, inline=False)
	msg = await channel.fetch_message(msg_id)
	await msg.edit(embed=embed)

@tasks.loop(minutes=2)
async def embedLeaderboard():
        channel = client.get_channel(CHANNEL_ID)
        msg_id = MESSAGE_ID
        embedDisc = "(Updates once you have left the server)"
        embed=discord.Embed(title=" Leaderboard", description=embedDisc, color=0xff00d0)
        playersTab = create_sqlList()
        playersTab.sort(key=takeSecond,reverse=True)
        playerField = "\n".join([f"{player} - {time} Mins" for player, time in playersTab])
        if playerField:
                embed.add_field(name="Players:",value=playerField, inline=False)
        msg = await channel.fetch_message(msg_id)
        await msg.edit(embed=embed)


client.run(TOKEN)
