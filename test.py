from dis import disco
from http import client
from pydoc import cli
from ssl import CHANNEL_BINDING_TYPES
import discord
import os
import json
import shutil
from discord.ext import commands
from discord import app_commands
import requests


with open("config.json", "r") as json_file:
    json_data = json.load(json_file)
token = json_data["token"]


intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message_delete(message):
    if message.author.bot == True:
        pass
    elif message.attachments:
        for attach in message.attachments:
            info = requests.head(attach.proxy_url)
            if int(info.headers["Content-Length"]) <= 8388608:
                await message.channel.send("{0}\n{1}".format(attach.url,attach.proxy_url))
            




client.run(token)