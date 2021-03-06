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

bot = discord.Client() #Creates Client
bot = commands.Bot(command_prefix=['!'])

def takeSecond(elem):
	return elem[2]

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
        player_topTen = []
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
        for index, i in enumerate(playerUnique): 
                for player,uptime,time in rawList:
                        if player == i:
                                player_uptime = player_uptime + uptime
#               print(f'{i}s uptime is {player_uptime}')
                if player_uptime > 10:
                    player_time = "{}h {}m".format(*divmod(player_uptime, 60))
                    player_final.append([i,player_time,player_uptime])
                player_uptime = 0
        return(player_final)

def getOnline():
    data = urlopen("http://10.0.20.3:8080/feed/dedicated-server-stats.xml?code=a51fce89c74b87cfbe526cbbc5ab18eb").read()
    Bs_data = BeautifulSoup(data, "xml")
    b_unique = Bs_data.find('Slots')
    value = b_unique.get('numUsed')
    return(value)

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

@bot.listen()
async def on_ready():
    countChannel.start()
    embedOnline.start()
    embedLeaderboard.start()
    print(f'{bot.user} is alive and listening for Discord events')


@tasks.loop(minutes=5)
async def countChannel():
    channel = bot.get_channel(947512883238031430)
    new_name = "???????Players Online {}/16???????".format(getOnline())
    print(new_name)
    await channel.edit(name=new_name)

@tasks.loop(minutes=2)
async def embedOnline():
	channel = bot.get_channel(947519131241033728)
	msg_id = 948287548638240809
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
        channel = bot.get_channel(950746385861476423)
        msg_id = 950755146449698886
        embedDisc = "(Updates once you have left the server)"
        embed=discord.Embed(title=" Top ten players of Season 5", description=embedDisc, color=0xff00d0)
        playersTab = create_sqlList()
        playersTab.sort(key=takeSecond,reverse=True)
        playersTopTen = playersTab[:10]
        playerField = "\n".join([f"{player} - {time}" for player, time, minutes in playersTopTen])
        if playerField:
                embed.add_field(name="Players:",value=playerField, inline=False)
        msg = await channel.fetch_message(msg_id)
        await msg.edit(embed=embed)
@tasks.loop(minutes=5)
async def maint_countChannel():
    channel = bot.get_channel(947512883238031430)
    new_name = "??????????
    print(new_name)
    await channel.edit(name=new_name)


@tasks.loop(minutes=2)
async def maint_embedLeaderboard():
        channel = bot.get_channel(950746385861476423)
        msg_id = 950755146449698886
        embedDisc = "??????????
        embed=discord.Embed(title=" Top ten players of Season 5", description=embedDisc, color=0xff00d0)
        msg = await channel.fetch_message(msg_id)
        await msg.edit(embed=embed)
@tasks.loop(minutes=2)
async def maint_embedOnline():
        channel = bot.get_channel(947519131241033728)
        msg_id = 948287548638240809
        embedDisc = "??????????
        embed=discord.Embed(title="Current Players", description=embedDisc, color=0xff00d0)
        msg = await channel.fetch_message(msg_id)
        await msg.edit(embed=embed)


@bot.command()
@commands.has_role(954147959904280586)
async def maint(ctx):
	print(countChannel.is_running())
	if countChannel.is_running():
		maintState = "Enabled"
		# Stopping the normal loops
		countChannel.cancel()
		embedOnline.cancel()
		embedLeaderboard.cancel()
		# Starting the Maint Loop
		maint_countChannel.start()
		maint_embedOnline.start()
		maint_embedLeaderboard.start()
	else:
		maintState = "Disabled"
		# Stopping the maint loops
		maint_countChannel.cancel()
		maint_embedOnline.cancel()
		maint_embedLeaderboard.cancel()
		# Starting the normal Loop
		countChannel.start()
		embedOnline.start()
		embedLeaderboard.start()

	await ctx.send(f'Maint Mode {maintState}')

bot.run(TOKEN)



