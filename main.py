import datetime
import json
from dis import disco
from http import client
from pydoc import cli
from ssl import CHANNEL_BINDING_TYPES
from typing import Any
from discord.ext.commands.core import Command
import requests

import discord
from discord import app_commands
from discord.ext import commands


import function
import io


intents=discord.Intents.all()
intents.message_content=True
bot=discord.Client(intents=intents)

bot = commands.Bot(command_prefix='!',intents=intents)


@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")




class CustomHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        embed=discord.Embed(color=discord.Color.dark_embed(),title="Help",
                             description=
                            "slash command\n- ping\n - check the bot's latency\n\nadministrator command\n- help <command>(optional)\n - send help embed\n - send <command>\'s help embed\n- setting <arg>\n - set the Logging channel with preset")
        await destination.send(embed=embed)

bot.help_command=CustomHelp()


@bot.tree.command(description="Check bot's response latency",name="ping")
async def ping(interaction: discord.Interaction):
    embed = discord.Embed(title="Pong!", description=f"Delay: {round(bot.latency*1000)} ms", color=0xFFFFFF)
    await interaction.response.send_message(embed=embed)

@bot.command()
async def setting(ctx, arg=""):
    
    data = {'message':"-m.d.c-m.e",'attachment':"-m.d.a",'voice':"-v.dm-v.jl",'exception':"-except"}
    topic = ctx.channel.topic
    print(topic)
    if arg in ['message','attachment','voice','exception']:
        if topic == None:
            await ctx.channel.edit(topic=data[arg])
            await ctx.send(f"{data[arg]} mode is set")
        else:
            await ctx.channel.edit(topic=topic+data[arg])
            await ctx.send(f"{data[arg]} mode is set")
    elif arg=="clear":
        await ctx.channel.edit(topic="")
    elif arg =="":
        await ctx.send("please add arg\n\nif you want to know arg? do !help setting")
    else:
        await ctx.send(f"{arg} is not exist")


@bot.event
async def on_message_delete(message):


    if message.author.bot == True:
        pass
    elif "-except" in str(message.channel.topic):
        pass

    else:
        now=datetime.datetime.utcnow().replace(tzinfo=None)
        if message.content or message.stickers:
        
            for ch in message.guild.text_channels:
                if "-message.delete.content" in str(ch.topic) or "-m.d.c" in str(ch.topic):
                    logging_channel=ch.id
            embed = discord.Embed(title="",
                    description="Message sent by {0.mention} deleted in {1.mention}\n\n{2}".format(message.author,message.channel,message.content), color=0xFF0000)
            embed.set_author(name="{0}#{1}".format(message.author.name, message.author.discriminator), icon_url="{}".format(message.author.display_avatar.url))
            if message.stickers:
                for st in message.stickers:
                    embed.set_image(url=f"{st.url}")
            async for entry in message.guild.audit_logs(limit=5,action=discord.AuditLogAction.message_delete):
                diff=now-entry.created_at.replace(tzinfo=None)
                if entry.extra.channel.id==message.channel.id and entry.target.id == message.author.id and diff.total_seconds()<20:
                    user=entry.user
                    embed.set_footer(icon_url=user.display_avatar.url,text=f"{user.name}#{user.discriminator}({user.id})")
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

            async for entry in message.guild.audit_logs(limit=5,action=discord.AuditLogAction.message_delete):
                diff=now-entry.created_at.replace(tzinfo=None)
                if entry.extra.channel.id==message.channel.id and entry.target.id == message.author.id and diff.total_seconds()<20:
                    user=entry.user
                    embed.set_footer(icon_url=user.display_avatar.url,text=f"{user.name}#{user.discriminator}({user.id})")

            channel = bot.get_channel(logging_channel)
            for attach in message.attachments:
                info = requests.head(attach.proxy_url)
                tier=message.guild.premium_tier
                if tier<2:
                    if int(info.headers["Content-Length"]) <= 0:
                        files_data.append(await attach.to_file())
                    
                    else:
                        data, name=await function.compression(attach,25)
                        files_data.append(discord.File(io.BytesIO(data),filename=name))
                    
                        
                elif tier==2:
                    if int(info.headers["Content-Length"]) <= 52428800:
                        files_data.append(await attach.to_file())
                elif tier==3:
                    if int(info.headers["Content-Length"]) <= 104857600:
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
async def on_voice_state_update(member, before, after):
    for ch in member.guild.text_channels:
        if "-voice.deaf_mute" in str(ch.topic) or "-v.dm" in str(ch.topic):
            logging_channel1=ch.id
        if "-voice.join_leave" in str(ch.topic) or "-v.jl" in str(ch.topic):
            logging_channel2=ch.id
    if before.mute != after.mute:
        if after.mute:
            state="Mute"
        else:
            state="Unmute"
        async for entry in member.guild.audit_logs(limit=1,action=discord.AuditLogAction.member_update):
            user=entry.user
        embed = discord.Embed(title="",
                description="{0.mention} had their voice state updated.\n**State**\n{1}\n**Voice Channel**\n{2.mention}".format(member,state,before.channel), color=0xFF0000)
        embed.set_author(name="{0}#{1}".format(member.name, member.discriminator), icon_url="{}".format(member.display_avatar.url))
        embed.set_footer(icon_url=user.display_avatar.url,text=f"{user.name}#{user.discriminator}({user.id})")
        channel = bot.get_channel(logging_channel1)
        await channel.send(embed=embed)
    if before.deaf != after.deaf:
        if after.deaf:
            state="Deaf"
        else:
            state="Undeaf"
        async for entry in member.guild.audit_logs(limit=1,action=discord.AuditLogAction.member_update):
            user=entry.user
        embed = discord.Embed(title="",
                description="{0.mention} had their voice state updated.\n**State**\n{1}\n**Voice Channel**\n{2.mention}".format(member,state,before.channel), color=0xFF0000)
        embed.set_author(name="{0}#{1}".format(member.name, member.discriminator), icon_url="{}".format(member.display_avatar.url))
        embed.set_footer(icon_url=user.display_avatar.url,text=f"{user.name}#{user.discriminator}({user.id})")
        channel = bot.get_channel(logging_channel1)
        await channel.send(embed=embed)
    if before.channel != after.channel:
        now = datetime.datetime.utcnow().replace(tzinfo=None)
        
        if not after.channel:
            state="leave"
            embed = discord.Embed(title="",
                description=f"{member.mention} {state} the voice channel\n**Channel**\n{before.channel.mention}", color=0xFF0000)
            async for entry in member.guild.audit_logs(limit=1,action=discord.AuditLogAction.member_disconnect):    
                created_at = entry.created_at.replace(tzinfo=None)
                diff = now - created_at
                if diff.total_seconds() < 10:
                    user=entry.user
                    embed.set_footer(icon_url=user.display_avatar.url,text=f"{user.name}#{user.discriminator}({user.id})")
        elif not before.channel:
            state="join"
            embed = discord.Embed(title="",
                description=f"{member.mention} {state} the voice channel\n**Channel**\n{after.channel.mention}", color=0xFF0000)
        else:
            state="move"
            embed = discord.Embed(title="",
                description=f"{member.mention} {state} from {before.channel.mention} to {after.channel.mention}\n**Current channel**\n{after.channel.mention}\n**Previous channel**\n{before.channel.mention}", color=0xFF0000)
            async for entry in member.guild.audit_logs(limit=1,action=discord.AuditLogAction.member_move):
                created_at = entry.created_at.replace(tzinfo=None)
                diff = now - created_at
                if diff.total_seconds() < 10 and entry.extra.channel.id == after.channel.id:
                    user=entry.user
                    embed.set_footer(icon_url=user.display_avatar.url,text=f"{user.name}#{user.discriminator}({user.id})")
        
        embed.set_author(name="{0}#{1}".format(member.name, member.discriminator), icon_url="{}".format(member.display_avatar.url))
        channel = bot.get_channel(logging_channel2)
        await channel.send(embed=embed)
            


with open("config.json", "r") as json_file:
    json_data = json.load(json_file)
token = json_data["token"]
bot.run(token)