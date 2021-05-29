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
from modules.encoding import Encoder
from modules.decoding import Decoder
from modules.hash import HashManager

bot = commands.Bot(command_prefix='z! ', description="Zer0 Bot")


@bot.event
async def on_ready():
    # Setting Gaming status
    await bot.change_presence(activity=discord.Game(name="Listening to z! helpme --> for help"))
    cve_updates.start()
    print("I'm ready")


@bot.command()
async def helpme(ctx):
    help_msg = '''
```
Zer0 Bot :
.
+-------------------------------------------------------------------------+
+    z! helpme          --> show this help message                        +
+    z! info            --> show server info                              +
+    z! ping            --> send a pong response                          +
+    z! encoding_help   --> show help about encoding strings              +
+    z! decoding_help   --> show help about decoding strings              +
+    z! hashing_help    --> show help about hash calculating              +
+    z! latest_cves 10  --> show 10 latest CVEs                           +
+    z! hackernews 5    --> show 5 latest hacker news                     + 
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
        await ctx.reply('Unknown command : z! helpme --> for help')


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
async def latest_cves(ctx, *, count=10):
    from modules.features import show_latest_cves
    await ctx.reply(embed=show_latest_cves(count))


# define show HackerNews' news function
@bot.command()
async def hackernews(ctx, count=5):
    from modules.features import hackerNews
    newsList = hackerNews(count)
    for news in newsList:
        await ctx.reply(embed=news)


@tasks.loop(seconds=45)
async def cve_updates():
    from modules.features import cve_update
    result = cve_update()
    channel = bot.get_channel(843229369585500201)
    if result != None :
        for item in result:
            await channel.send(embed=item)


bot.run(token)
