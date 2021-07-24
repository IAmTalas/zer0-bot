import requests
import json
import dotenv
from datetime import datetime
from subscriptions import get_subscriptions
import discord

# get feedly creds
feed_creds = dotenv.dotenv_values('.env.feed')

# filter website by their topic
def topic_filter(json, label):
    try:
        return [item for item in json if any(l in item['topics'] for l in label)]
    except KeyError:
        pass


# filter websites and sort them
# label filter is list of labels, that you can apply it to filter website type
def subscribtions_list(label_filter=[], sort_option="subscribers"):
    get_subscriptions()
    # read websites list from file
    with open('subscriptions.json','rb') as file:
        rev = True
        subscriptions_json = json.load(file)
        if sort_option == "velocity":
            rev = False
        subscriptions_json = sorted(subscriptions_json, key=lambda x : x[f'{sort_option}'],reverse=rev)
        # if lable is given, apply it
        if label_filter != []:
            subscriptions_json = topic_filter(subscriptions_json, label_filter)
    for item in subscriptions_json:
        yield item

 
def render_msg(site_count = 10, message_count = 10, label_filter=[], timestamp_filter = False , timestamp = 0 ):

    msg_list = []

    for index, subscribtions_website in enumerate(subscribtions_list(label_filter),1):

        headers = {
            'Authorization': feed_creds['TOKEN'].strip()
        }

        params = (
            ('streamId', subscribtions_website['id']),
            ('count', message_count),
        )

        response = requests.get('https://cloud.feedly.com/v3/streams/contents', headers=headers, params=params)

        for msg_json in response.json()['items']:
            # if timestamp_filter applied check the last time and msg time stamp
            if timestamp_filter == True and timestamp != 0:
                if msg_json['origin']['published'] > timestamp:
                    pass
                else:
                    continue
            # 'website':msg_list['origin']['htmlUrl']
            try:
                msg_list.append({'title':msg_json['title'], 'website':subscribtions_website['title'], 'author':msg_json['author'], 'url':msg_json['alternate'][0]['href'], 'published':msg_json ['published']})
            except KeyError:
                pass
        
        if index == site_count:
            break 
    # sort message from old to new 
    msg_list = sorted(msg_list, key=lambda x: float(x['published']), reverse=False)

    for msg in msg_list:
        renderd_msg = discord.Embed(title=msg['title'],colour=discord.Color.random())
        renderd_msg.add_field(name="Source", value=msg['url'])
        renderd_msg.set_author(name=msg['author'])
        renderd_msg.set_footer(text=msg['published'])
                
        yield renderd_msg
