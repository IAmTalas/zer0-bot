import html as htm
import binascii
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


@bot.command()
async def b64(ctx, t, msg):
    print(t, msg)
    msg = str(msg)
    if t == "encode":
        await ctx.reply("```{}```".format(base64.b64encode(msg.encode('utf-8')).decode("utf-8")))
    if t == "decode":
        await ctx.reply("```{}```".format(str(base64.b64decode(msg), "UTF-8")))


@bot.command()
async def html(ctx, t, msg):
    print(htm.unescape(msg))
    print(htm.escape(msg))
    # if t == "encode":
    #     await ctx.reply("```{}```".format(8))
    # if t == "decode":
    #     await ctx.reply("```{}```".format(8))


@bot.command()
async def hex(ctx, t, msg):
    if t == "encode":
        await ctx.reply("```{}```".format(binascii.hexlify(bytes(msg, 'utf-8'))))
    if t == "decode":
        await ctx.reply("```{}```".format(''.join([chr(int(''.join(c), 16)) for c in zip(msg[0::2], msg[1::2])])))


@bot.command()
async def url(ctx, t, msg):
    if t == "encode":
        await ctx.reply("```{}```".format(urllib.parse.unquote(msg)))
    if t == "decode":
        await ctx.reply("```{}```".format(urllib.parse.quote(msg)))


@bot.command()  # context is automatically passed in rewrite
async def readURL(ctx):
    attachment = ctx.message.attachments[0]  # gets first attachment that user
    # sent along with command
    print(attachment.url)


@bot.command()
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Lorem Ipsum asdasd",
                          timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server Owner", value=f"GOD")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    # embed.set_thumbnail(url=f"{ctx.guild.icon}")
    embed.set_thumbnail(url="https://pluralsight.imgix.net/paths/python-7be70baaac.png")

    await ctx.send(embed=embed)


@bot.command()
async def ping(ctx, msg):
    await ctx.send(msg.mentions)


@bot.command()
async def welcome(ctx, user: discord.Member):
    await ctx.send(f'{user.mention} welcome to the server (and more welcome stuff here).')


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name="Tutorials", url="http://www.twitch.tv/accountname"))
    print('My Ready is Body')


@bot.listen()
async def on_message(message):
    print(message.mentions)
    if "tutorial" in message.content.lower():
        # in this case don't respond with the word "Tutorial" or you will call the on_message event recursively
        await message.channel.send('This is that you want http://google.com/')
        await bot.process_commands(message)
    if message.attachments[0].url.endswith('exe') or message.attachments[0].url.endswith('pdf') or message.attachments[
        0].url.endswith('rar') or message.attachments[0].url.endswith('zip') or message.attachments[0].url.endswith(
            'jar') or message.attachments[0].url.endswith('vb') or message.attachments[0].url.endswith('vbe'):
        embed = discord.Embed()
        embed.description = "         ⚠ BE CAREFUL ,THIS FILE MAY BE DANGEROUS  ⚠\n⭕HOW ABOUT TRYING TO SCAN IT ? [virustotal](https://https://www.virustotal.com/)⭕"
        await message.reply(embed=embed)


bot.run(os.getenv('TOKEN'))
