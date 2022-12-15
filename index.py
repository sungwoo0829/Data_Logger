import datetime
import json
import os
import shutil
from dis import disco
from http import client
from pydoc import cli
from ssl import CHANNEL_BINDING_TYPES
import requests
import json
import pycord
import discord
from discord.commands import Option

intents=discord.Intents.all()
intents.message_content=True
bot=discord.Bot(intents=intents)


@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")

@bot.slash_command(description="Check bot's response latency")
async def ping(ctx):
    embed = discord.Embed(title="Pong!", description=f"Delay: {bot.latency} seconds", color=0xFFFFFF)
    embed.set_footer(text="Embed Footer")
    await ctx.respond(embed=embed)



@bot.slash_command(description="Kick user whose account has been created for a set period of time (0 means don't kick, default is 0)")
async def autokick_created_at(ctx, days: Option(int, "set day")):
    if not ctx.author.guild_permissions.kick_members:
        return
    with open("guild.json","r") as json_file:
        json_data = json.load(json_file)

    if f"{ctx.guild.id}" not in json_data.keys():
        json_data[f"{ctx.guild.id}"]={"autokick_created_at":days}
    if "autoskick_created_at" not in json_data[f"{ctx.guild.id}"].keys():
        json_data[f"{ctx.guild.id}"]={"autokick_created_at":days}
    else:
        json_data[f"{ctx.guild.id}"]["autokick_created_at"]=days
    with open ("guild.json","w") as json_file:
        json.dump(json_data, json_file, indent=2)
    await ctx.respond(f"set {days} days!")









@bot.event
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
            channel = bot.get_channel(logging_channel)
            await channel.send(embed=embed)


        



        if message.attachments:

        

            for ch in message.guild.text_channels:
                if "-message.delete.attachment" in str(ch.topic) or "-m.d.a" in str(ch.topic):
                    logging_channel=ch.id

            embed = discord.Embed(title="",
                    description="Message sent by {0.mention} deleted in {1.mention}".format(message.author,message.channel), color=0xFF0000)
            embed.set_author(name="{0}#{1}".format(message.author.name, message.author.discriminator), icon_url="{}".format(message.author.display_avatar.url))

            files_data=[]

            channel = bot.get_channel(logging_channel)
            for attach in message.attachments:
                info = requests.head(attach.proxy_url)
            
                if int(info.headers["Content-Length"]) <= 8388608:
                    files_data.append(await attach.to_file())
                elif message.guild.premium_tier==2 and int(info.headers["Content-Length"]) <= 52428800:
                    files_data.append(await attach.to_file())
                elif message.guild.premium_tier==3 and int(info.headers["Content-Length"]) <= 104857600:
                    files_data.append(await attach.to_file())
            await channel.send(embed=embed,files=files_data)

        



        

@bot.event
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
        channel = bot.get_channel(logging_channel)
        await channel.send(embed=embed)

@bot.event
async def on_member_join(member):
    with open("guild.json", "r") as json_file:
        json_data = json.load(json_file)
    if "{}".format(member.guild.id) in json_data.keys() and "autokick_created_at" in json_data["{}".format(member.guild.id)].keys():
        now = datetime.datetime.now().replace(tzinfo=None)
        created_at = member.created_at.replace(tzinfo=None)
        diff = now - created_at
        if diff.days < json_data["{}".format(member.guild.id)]["autokick_created_at"]:
            if member.dm_channel:
                await member.dm_channel.send("User whose account has been created for "+str(json_data["{}".format(member.guild.id)]["autokick_created_at"])+"days can join `{}`".format(member.guild.name))
            else:
                await member.create_dm()
                await member.dm_channel.send("User whose account has been created for "+str(json_data["{}".format(member.guild.id)]["autokick_created_at"])+"days can join `{}`".format(member.guild.name))
            await member.kick(reason="this account is created at less than"+str(json_data["{}".format(member.guild.id)]["autokick_created_at"])+"days")

@bot.event
async def on_voice_state_update(member, before, after):
    for ch in member.guild.text_channels:
        if "-voice.deaf_mute" in str(ch.topic) or "-v.dm" in str(ch.topic):
            logging_channel1=ch.id
        if "-voice.join_leave" in str(ch.topic) or "-v.jl" in str(ch.topic):
            logging_channel2=ch.id
    if before.self_mute != after.self_mute:
        return
    if before.self_deaf != after.self_deaf:
        return
    if before.self_stream != after.self_stream:
        return
    if before.self_video != after.self_video:
        return
    if before.deaf != after.deaf:
        if after.deaf:
            state="Mute"
        else:
            state="Unmute"
        discord.Guild.audit_logs(limit=1,action="member_update")
        user=member.guild.audit_logs(limit=1,action="member_update").user
        embed = discord.Embed(title="",
                description="{0.mention} had their voice state updated.\n**State**\n{1}\n**Voice Channel**\n{2.mention}".format(member,state,before.channel), color=0xFF0000)
        embed.set_author(name="{0}#{1}".format(member.name, member.discriminator), icon_url="{}".format(member.display_avatar.url))
        embed.set_footer(icon_url=user.display_avatar.url,text=f"{user.mention}")
        channel = bot.get_channel(logging_channel1)
        await channel.send(embed=embed)

        



with open("config.json", "r") as json_file:
    json_data = json.load(json_file)
token = json_data["token"]
bot.run(token)
