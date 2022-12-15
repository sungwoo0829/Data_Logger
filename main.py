import datetime
import json
import os
import shutil
from dis import disco
from http import client
from pydoc import cli
from ssl import CHANNEL_BINDING_TYPES

import discord
import requests
from discord import app_commands
from discord.ext import commands

with open("config.json", "r") as json_file:
    json_data = json.load(json_file)
token = json_data["token"]

intents = discord.Intents.all()
intents.message_content = True


client = discord.Client(intents=intents)
bot = commands.Bot(intents=intents,command_prefix="$")



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@bot.command(name="first_slash", guild_ids=[1007625110083076146]) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def first_slash(ctx): 
    await ctx.respond("You executed the slash command!")

@client.event
async def on_message(message):
    
    if message.author == client.user:
        return
    elif message.content.startswith('$help'):
        message.channel.send("nothing here")





@client.event
async def on_message_delete(message):


    if message.author.bot == True:
        pass
    elif "-except" in str(message.channel.topic):
        pass

    else:

        if message.content:
        
            for ch in message.guild.text_channels:
                if "-message.delete.content" in str(ch.topic) or "-m.d.c" in str(ch.topic):
                    logging_channel=ch.id
            embed = discord.Embed(title="",
                    description="Message sent by {0.mention} deleted in {1.mention}\n\n{2}".format(message.author,message.channel,message.content), color=0xFF0000)
            embed.set_author(name="{0}#{1}".format(message.author.name, message.author.discriminator), icon_url="{}".format(message.author.display_avatar.url))
            channel = client.get_channel(logging_channel)
            await channel.send(embed=embed)


        



        if message.attachments:

        

            for ch in message.guild.text_channels:
                if "-message.delete.attachment" in str(ch.topic) or "-m.d.a" in str(ch.topic):
                    logging_channel=ch.id

            embed = discord.Embed(title="",
                    description="Message sent by {0.mention} deleted in {1.mention}".format(message.author,message.channel), color=0xFF0000)
            embed.set_author(name="{0}#{1}".format(message.author.name, message.author.discriminator), icon_url="{}".format(message.author.display_avatar.url))

            files_data=[]

            channel = client.get_channel(logging_channel)
            for attach in message.attachments:
                info = requests.head(attach.proxy_url)
            
                if int(info.headers["Content-Length"]) <= 8388608:
                    files_data.append(await attach.to_file())
                elif message.guild.premium_tier==2 and int(info.headers["Content-Length"]) <= 52428800:
                    files_data.append(await attach.to_file())
                elif message.guild.premium_tier==3 and int(info.headers["Content-Length"]) <= 104857600:
                    files_data.append(await attach.to_file())
            await channel.send(embed=embed,files=files_data)

        



        

@client.event
async def on_message_edit(message_before,message_after):


    if message_before.author.bot == True:
        pass
    elif "-except" in str(message_before.channel.topic):
        pass

    elif message_before.content != message_after.content:
        for ch in message_before.guild.text_channels:
            if "-message.edit" in str(ch.topic) or "-m.e" in str(ch.topic):
                logging_channel=ch.id

        embed = discord.Embed(title="",
                description="Message sent by {0.mention} edited in {1.mention}\n\n**Before** :\n{2}\n\n**After** :\n{3}".format(message_before.author,message_before.channel,message_before.content,message_after.content), color=0xFF0000)
        embed.set_author(name="{0}#{1}".format(message_before.author.name, message_before.author.discriminator), icon_url="{}".format(message_before.author.display_avatar.url))
        channel = client.get_channel(logging_channel)
        await channel.send(embed=embed)

@client.event
async def on_member_join(member):
    with open("guild.json", "r") as json_file:
        json_data = json.load(json_file)
    if "{}".format(member.guild.id) in json_data.keys() and "autokick_created_at" in json_data["{}".format(member.guild.id)].keys():
        diff = datetime.now() - member.created_at
        if diff.days < json_data["{}".format(member.guild.id)]["autokick_created_at"]:
            await member.kick(reason="this account is created at less than"+json_data["{}".format(member.guild.id)]["autokick_created_at"]+"days")
            await member.dm_channel.send("User whose account has been created for "+json_data["{}".format(member.guild.id)]["autokick_created_at"]+"days can join `{}`".format(member.guild.name))
        else:
            pass
    else:
        pass






client.run(token)

