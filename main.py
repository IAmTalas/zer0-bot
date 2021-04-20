import discord
import os
import re
import urllib.parse
import base64


def getQuote(message):
    regex = r"\"(.*)\""
    match = re.search(regex, message)
    return match.group(1)


client = discord.Client()


@client.event
async def on_ready():
    print('we have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content
    if message.content.startswith("!hello"):
        await message.reply("hello {}".format(message.author))


    if "!z en-b64" in msg:
        msg = msg.replace('!z en-b64', '')
        msg = getQuote(msg)
        await message.reply("```{}```".format
                            (base64.b64encode(msg.encode('utf-8')).decode("utf-8")))
        
        
        
    if "!z de-b64" in msg:
        msg = msg.replace('!z de-b64', '')
        msg = getQuote(msg)
        print(msg)
        await message.reply("{}".format
                            (str(base64.b64decode(msg),"UTF-8")))



    if "!z de-url" in msg:
        msg = msg.replace('!z de-url', '')
        msg = getQuote(msg)
        print(msg)
        await message.reply("{}".format(urllib.parse.unquote(msg)))


    if "!z en-url" in msg:
        msg = msg.replace('!z en-url', '')
        msg = getQuote(msg)
        print(msg)
        await message.reply("```{}```".format(urllib.parse.quote(msg)))

client.run(os.getenv('TOKEN'))
