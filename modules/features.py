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

    if not os.path.exists('modules/events.json'):
        with open('events.json', 'w') as file:
            file.write('[]')

    remove_expired_event()

    with open('modules/events.json','r+') as file:
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

def remove_expired_event():
    with open('modules/events.json', 'r' ,encoding='utf-8') as file:
        file_json = json.load(file)
        valid_list = [item for item in file_json if not (datetime.datetime.strptime(item['time'], r"%Y-%m-%d %H:%M") - datetime.datetime.utcnow()).days <= -1 ]
    with open('modules/events.json', 'w+' ,encoding='utf-8') as file:    
        file.write(json.dumps(valid_list, ensure_ascii=False ,indent=4))

def send_request(url):
    res =  requests.get(url=url, stream=True, headers={'limit': '30'}).json()['results']
    for index in range(res):
        res[index].pop('vulnerable_configuration_cpe_2_2', None)
        res[index].pop('vulnerable_configuration', None)
        res[index].pop('vulnerable_product', None)
        res[index].pop('references', None)

def render_cve_embed(data):
    embed_items = []

    for cve in data:
        print(cve)
        if cve['cvss'] != None:    
            if float(cve['cvss']) == 0:
                color = discord.Color.green()
            elif float(cve['cvss']) in range(1,4):
                color = discord.Color.from_rgb(255,255,0)
            elif float(cve['cvss']) in range(4,8):
                color = discord.Color.orange()
            elif float(cve['cvss']) in range(7,9):
                color = discord.Color.red()
            else:
                color = discord.Color.from_rgb(165,0,0)
        else: 
            color =discord.Color(255,255,255)    
        embed = discord.Embed(title=f"{cve['id']}", description=f"Published : {cve['Published']}",color=color)
        embed.add_field(name="summary", value=f"{cve['summary'][:600]}")
        embed.add_field(name="CVSS", value=f"{cve['cvss']}")
        embed_items.append(embed)
    return embed_items

def check_cve_update():
    global init_request
    update_list = []
    req = send_request("https://cve.circl.lu/api/query")
    print(datetime.datetime.now())
    if not req[0]['id'] == init_request[0]['id'] :
        for item in req:
            if item['id'] == init_request[0]['id'] :
                break
            update_list.append(item)
        init_request = req
        return render_cve_embed(update_list)

init_request = send_request("https://cve.circl.lu/api/query")

def show_latest_cves():
    global init_request
    return render_cve_embed(data=init_request)
