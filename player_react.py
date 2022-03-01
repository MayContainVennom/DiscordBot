# bot.py
import os
import random
import discord

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(message.author)
    user = "[Player Name]]"
    if str(message.author) == str(user):
        print("Sending Eggplant")
        emoji = "🍆"
        await message.add_reaction(emoji)

client.run(TOKEN)