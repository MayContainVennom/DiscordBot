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

def getOnline():
    data = urlopen(SERVER_XML).read()
    Bs_data = BeautifulSoup(data, "xml")
    b_unique = Bs_data.find('Slots')
    value = b_unique.get('numUsed')
    return(value)

# put the test.start() in the on_ready event
@client.listen()
async def on_ready():
    # start test loop
    test.start()
         
    # ready message print to console
    print(f'{client.user} is alive and listening for Discord events')


@tasks.loop(minutes=5)
async def test():
    channel = client.get_channel(PLAYER_CHANNEL)
    new_name = "✅Players Online {}/16✅".format(getOnline())
    print(new_name)
    await channel.edit(name=new_name)


client.run(TOKEN)
