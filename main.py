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
from modules.encoding import Encoder
from modules.decoding import Decoder

bot = commands.Bot(command_prefix='z! ', description="Zer0 Bot")

@bot.event
async def on_ready():
    # Setting Gaming status
    await bot.change_presence(activity=discord.Game(name="Listening to z! helpme --> for help"))
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
+-------------------------------------------------------------------------+
.
```
    '''
    await ctx.send(help_msg)

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

# generally handling errors
# @bot.event
# async def on_command_error(ctx ,error):
#     if isinstance(error ,commands.MissingRequiredArgument):
#         await ctx.send('Fill the required arguments pls')


@bot.command()
async def ping(ctx):
    await ctx.send('pong :ping_pong:')

# define encoding function
@bot.command()
async def en(ctx,*,msg):
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
            await ctx.send(temp_msg)

@bot.command()
async def encoding_help(ctx,*,msg=None):
    encoder = Encoder()
    await ctx.send(encoder.show_help())

# handle encode function errors
@en.error
async def encode_error(ctx ,error):
    if isinstance(error ,commands.MissingRequiredArgument):
        await ctx.send('specify the encoding type you want --> z! en base64 your_string')

# define decoding function
@bot.command()
async def de(ctx,*,msg):
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
            await ctx.send(temp_msg)

@bot.command()
async def decoding_help(ctx,*,msg=None):
    decoder = Decoder()
    await ctx.send(decoder.show_help())

# handle decode function errors
@de.error
async def decode_error(ctx ,error):
    if isinstance(error ,commands.MissingRequiredArgument):
        await ctx.send('specify the decoding type you want --> z! de base64 your_string')


bot.run(token)
