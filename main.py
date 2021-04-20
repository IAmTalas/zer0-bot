#!/usr/bin/env python3

'''
Zer0 Discord Bot
'''

try:
    with open('token.txt','r') as token_file:
        token = token_file.read()

except FileNotFoundError:
    with open('token.txt','w') as token_file:
        print('put the token inside token.txt file')
        exit()

import discord
from discord.ext import commands
import datetime

bot = commands.Bot(command_prefix='z! ', description="Zer0 Bot")

@bot.command()
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Zer0 Bot",
                          timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    # embed.set_thumbnail(url=f"{ctx.guild.icon}")
    embed.set_thumbnail(url="https://pluralsight.imgix.net/paths/python-7be70baaac.png")
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name="Tutorials", url="http://www.twitch.tv/accountname"))
    print("I'm ready")

bot.run(token)