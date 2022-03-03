import os
import random
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

def getOnline():
    data = urlopen("").read()
    Bs_data = BeautifulSoup(data, "xml")
    b_unique = Bs_data.find('Slots')
    value = b_unique.get('numUsed')
    return(value)
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
@client.listen()
async def on_ready():
    countChannel.start()
    embedNew.start()
    print(f'{client.user} is alive and listening for Discord events')

@tasks.loop(minutes=5)
async def countChannel():
    channel = client.get_channel("")
    new_name = "✅Players Online {}/16✅".format(getOnline())
    print(new_name)
    await channel.edit(name=new_name)
@tasks.loop(minutes=2)
async def embedNew():
	channel = client.get_channel("")
	msg_id = ""
	embedDisc = "Online Players {}/16".format(getOnline())
	embed=discord.Embed(title="Realistic Farming UK Server", description=embedDisc, color=0xff00d0)
	playersTab = getPlayers()
	playerField = "\n".join([f"{player} - {time} Mins" for player, time in playersTab])
	embed.add_field(name="Players:",value=playerField, inline=False)
	msg = await channel.fetch_message(msg_id)
	await msg.edit(embed=embed)

client.run(TOKEN)


