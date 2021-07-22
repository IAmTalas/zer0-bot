'''
Module for adding features
'''
import requests
import discord
import os
import pytz
import datetime
import json

def iran_to_utc(time):
    local_time = pytz.timezone("Asia/Tehran")
    naive_datetime = datetime.datetime.strptime (time, r"%Y-%m-%d %H:%M")
    local_datetime = local_time.localize(naive_datetime, is_dst=None)
    utc_datetime = local_datetime.astimezone(pytz.utc)
    return utc_datetime

def utc_to_iran(time):
    utc_time = datetime.datetime.strptime(time, r"%Y-%m-%d %H:%M")
    tz = pytz.timezone('Asia/Tehran')
    iran_local = utc_time.replace(tzinfo=pytz.utc).astimezone(tz)
    return iran_local

def add_upcomming(title, date):
    '''
    add upcomming events to events.json
    '''

    data = {"title" : title, "time" : str(iran_to_utc(date))}

    if not os.path.exists('events.json'):
        with open('events.json', 'w') as file:
            file.write('[]')

    with open('events.json','r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data.append(data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)
 

    embed = discord.Embed(title=f"New Event : {title}", colour=discord.Color.random(), description=" @everyone Wind up your clocks !")
    embed.set_footer(text=date)
    return embed