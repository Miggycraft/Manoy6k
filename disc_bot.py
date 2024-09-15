import discord
import os
import asyncio
import random as rng
import json
from dotenv import load_dotenv

#custom emotes
EMOTES = {}
with open('stored_emotes.json', 'r') as file:
    EMOTES = json.load(file)

USERS = {}
with open('stored_users.json', 'r') as file:
    USERS = json.load(file)

#checks all user for reactions


load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

#hadles custom functions?
async def delete_arr(arr):
    for x in arr:
        await x.delete()

async def gacha_mechanic(message):
    temps = []
    temps.append(await message.channel.send('pulling...'))
    temps.append(await message.channel.send('https://tenor.com/view/genshin-impact-pull-wish-5star-five-star-gif-25193765'))
    await asyncio.sleep(5.9)

    await delete_arr(temps)

    emote_name, emote_id = rng.choice(list(EMOTES.items()))
    emote_id = client.get_emoji(emote_id)
    await message.channel.send(f'You got {emote_name} {emote_id}')
    await update_react(message.author, emote_id)

async def update_react(user, emote_id):
    USERS[str(user.id)] = str(emote_id)

async def reactionary(message):
    if str(message.author.id) in USERS.keys():
        # should not react to non gacha players
        if USERS[str(message.author.id)] == 'NULL':
            return
        await message.add_reaction(USERS[str(message.author.id)])
    else:
        USERS[str(message.author.id)] = 'NULL'

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return

    #reaction here
    await reactionary(message)

    #stops reactionary
    if message.content.startswith('.manoy samok'):
        USERS[str(message.author.id)] = 'NULL'
        await message.delete()
        temp = await message.channel.send(f'yawa ok :(')
        await asyncio.sleep(1.0)
        await temp.delete()

    #gacha mechanic
    if message.content.startswith('.manoy pull'):
        await gacha_mechanic(message)



#runs only once
client.run(TOKEN)

#saves everything
with open('stored_users.json', 'w') as file:
    json.dump(USERS, file)