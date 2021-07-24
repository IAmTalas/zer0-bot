import dotenv 
import requests
import os
import dotenv

def get_subscriptions()-> None:

    if not os.path.exists('.env.feed') :
        print('[!] Put your feed creds in ".env.feed" .')
        with open('.env.feed', 'w') as file:
            file.write("TOKEN=")
        exit()
    else:
        feed_creds = dotenv.dotenv_values(r".env.feed")
        if feed_creds['TOKEN'] == "" :
            print('[!] Put your feed creds in ".env.feed" .')
            exit()

    if not os.path.exists('subscriptions.json') :

        headers = {
            'Authorization': feed_creds['TOKEN'].strip()
        }

        response = requests.get('https://cloud.feedly.com/v3/subscriptions', headers=headers)
        
        with open('subscriptions.json', 'wb') as file:
            file.write(response.content)