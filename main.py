#!/usr/bin/env python3

'''
Zer0 Discord Bot
'''

try:
    with open('token.txt', 'r') as token_file:
        token = token_file.read()

except FileNotFoundError:
    with open('token.txt', 'w') as token_file:
        print('put the token inside token.txt file')
        exit()

import discord
from discord.ext import commands ,tasks
import datetime
import time
from modules.encoding import Encoder
from modules.decoding import Decoder
from modules.hash import HashManager
import asyncio

bot = commands.Bot(command_prefix='! ', description="Zer0 Bot")


@bot.event
async def on_ready():
    # Setting Gaming status
    await bot.change_presence(activity=discord.Game(name="Listening to z! helpme --> for help"))
    cve_updates.start()
    news.start()
    print("I'm ready")


@bot.command()
async def helpme(ctx):
    help_msg = '''
```
Zer0 Bot :
.
+-------------------------------------------------------------------------+
+    ! helpme          --> show this help message                        +
+    ! info            --> show server info                              +
+    ! ping            --> send a pong response                          +
+    ! encoding_help   --> show help about encoding strings              +
+    ! decoding_help   --> show help about decoding strings              +
+    ! hashing_help    --> show help about hash calculating              +
+-------------------------------------------------------------------------+
.
```
    '''
    await ctx.reply(help_msg)


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
    await ctx.reply(embed=embed)


# generally handling errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply('Unknown command : ! helpme --> for help')


@bot.command()
async def ping(ctx):
    await ctx.reply('pong :ping_pong:')


# define encoding function
@bot.command()
async def en(ctx, *, msg):
    if msg:
        encoder = Encoder(msg)
        result = encoder.encode()
        temp_msg = '''
```
word : {}
encoded : {}
```
'''
        try:
            temp_msg = temp_msg.format(result['word'], result['encoded'])
        except KeyError:
            pass
        else:
            await ctx.reply(temp_msg)


@bot.command()
async def encoding_help(ctx, *, msg=None):
    encoder = Encoder()
    await ctx.reply(encoder.show_help())


# handle encode function errors
@en.error
async def encode_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply('specify the encoding type you want --> z! en base64 your_string')


# define decoding function
@bot.command()
async def de(ctx, *, msg):
    if msg:
        decoder = Decoder(msg)
        result = decoder.decode()
        temp_msg = '''
```
word : {}
decoded : {}
```
'''
        try:
            temp_msg = temp_msg.format(result['word'], result['decoded'])
        except KeyError:
            pass
        else:
            await ctx.reply(temp_msg)


@bot.command()
async def decoding_help(ctx, *, msg=None):
    decoder = Decoder()
    await ctx.reply(decoder.show_help())


# handle decode function errors
@de.error
async def decode_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply('specify the decoding type you want --> z! de base64 your_string')


# define hash calculating function
@bot.command()
async def hash(ctx, *, msg):
    if msg:
        hash_manager = HashManager(msg)
        result = hash_manager.calculate_hash()
        temp_msg = '''
    ```
    word : {}
    hashed : {}
    ```
    '''
        try:
            temp_msg = temp_msg.format(result['word'], result['hash'])
        except KeyError:
            pass
        else:
            await ctx.reply(temp_msg)

@bot.command()
async def hashing_help(ctx, *, msg=None):
    hash_manager = HashManager()
    await ctx.reply(hash_manager.show_help())


# define show latest CVEs function
@bot.command()
async def latest_cves(ctx):
    from modules.features import show_latest_cves
    embeds = show_latest_cves()
    for embed in embeds:
        await ctx.reply(embed=embed)
        await asyncio.sleep(3)


@bot.command()
async def newupcomming(ctx,*arg):
    from modules.features import add_upcomming
    embed_item = add_upcomming(arg[0], arg[1])
    await ctx.reply(embed=embed_item)


@tasks.loop(minutes=5)
async def cve_updates():
    from modules.features import check_cve_update
    channel = bot.get_channel(" YOUR CHANELL ID ")
    embeds = check_cve_update()
    if embeds != None :
        for embed in embeds:
            await channel.send(embed=embed)
            await asyncio.sleep(3)

last_timestamp = time.time()
@tasks.loop(hours=5)
async def news():
    global last_timestamp
    from modules.feeder import render_msg
    channel = bot.get_channel(" YOUR CHANELL ID ")
    embeds = render_msg(site_count=30, message_count=15, label_filter=['security'], timestamp_filter=True, timestamp=last_timestamp)
    if embeds != None :
        for embed in embeds:
            await channel.send(embed=embed)
            await asyncio.sleep(3)
    last_timestamp = time.time()


bot.run(token)
