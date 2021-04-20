import discord
import os
import re
import urllib.parse
import base64
import asyncio
from discord.ext import commands
import datetime



def getQuote(message):
    regex = r"\"(.*)\""
    match = re.search(regex, message)
    return match.group(1)


bot = commands.Bot(command_prefix='>', description="This is a Helper Bot")


# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     msg = message.content
#     await bot.process_commands(message)
#     if message.content.startswith("!hello"):
#         await message.reply("hello {}".format(message.author))


@bot.command()
async def enb64(ctx,*,msg):
    await ctx.reply("```{}```".format
                        (base64.b64encode(msg.encode('utf-8')).decode("utf-8")))

@bot.command()
def deb64(ctx,*,msg):
    msg = getQuote(ctx,*,msg)
    await ctx.reply("```{}```".format
                        (str(base64.b64decode(msg), "UTF-8")))

@bot.command()
def deurl(ctx,*,msg):
    await ctx.reply("```{}```".format(urllib.parse.unquote(msg)))

@bot.command()
def enurl(ctx,*,msg):
    await ctx.reply("```{}```".format(urllib.parse.quote(msg)))



@bot.command()
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Lorem Ipsum asdasd",
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
    print('My Ready is Body')


@bot.listen()
async def on_message(message):
    if "tutorial" in message.content.lower():
        # in this case don't respond with the word "Tutorial" or you will call the on_message event recursively
        await message.channel.send('This is that you want http://google.com/')
        await bot.process_commands(message)

bot.run(os.getenv('TOKEN'))
