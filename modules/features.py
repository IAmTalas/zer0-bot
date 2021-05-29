'''
Module for adding features
'''
from bs4 import BeautifulSoup
import requests
import discord
from tabulate import tabulate
import re
import os



def show_latest_cves(count):

    if count > 19 :
        count = 19
    if count < 1 :
        count = 10

    url = 'https://cve.circl.lu/'

    cve_req = requests.get(url)
    content = str(cve_req.content)
    soup = BeautifulSoup(content, 'html.parser')
    content = soup.findAll('tr')

    number_of_cves = 0
    cve_names = []
    for l in content:
        if number_of_cves >= count:
            break
        if l.get('id'):
            number_of_cves += 1
            cve_names.append(l.get('id'))

    cvss_pattern = '''<td data-type="CVSS" data-value="(.*?)">'''
    summary_pattern = '''<div rel=".*" title="(.*?)">'''
    published_at_pattern = '''<td data-type="PUBLISHED" data-value="(.*?)">'''

    cves_info = []

    for cve in cve_names:
        specific_cve = soup.find(id=cve)
        specific_cve = str(specific_cve)
        # data
        cve_name = cve
        cve_link = "[link]({})".format(url + 'cve/' + cve)
        cvss = re.findall(cvss_pattern, specific_cve)
        if len(cvss) != 1:
            cvss = 'None'
        else:
            cvss = cvss[0]

        summary = re.findall(summary_pattern, specific_cve)
        if len(summary) != 1:
            summary = 'Empty'
        else:
            summary = summary[0]

        published_at = re.findall(published_at_pattern, specific_cve)
        if len(published_at) != 1:
            published_at = 'None'
        else:
            published_at = published_at[0]

        if summary:
            summary = summary[0:135]

        cves_info.append([cve_name, cvss, summary, published_at, cve_link])

    embed = discord.Embed()
    for c in cves_info:
        embed.add_field(name=c[0] ,value='CVSS : {}\n{} \nPublished At : {} \n{}'.format(c[1],c[2],c[3],c[4]))
    return embed


'''
Hacker news top 10 news
'''


def hackerNews(count=10):
    newsList = []
    if count <= 20:
        topNews = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty")
        for news in topNews.json()[:count]:
            newsJson = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{news}.json?print=pretty").json()
            embed = discord.Embed(title=f"{newsJson['title']}", description=f"by {newsJson['by']}",
                                  color=discord.Color.red())
            embed.add_field(name="Link", value=f"{newsJson['url']}")
            newsList.append(embed)
        return newsList





newTable = []
oldTable = []
newList = []

data = {
    "draw": "1",
    "columns[0][data]": "blank",
    "columns[0][name]": "",
    "columns[0][searchable]": "false",
    "columns[0][orderable]": "false",
    "columns[0][search][value]": "",
    "columns[0][search][regex]": "false",
    "columns[1][data]": "id",
    "columns[1][name]": "",
    "columns[1][searchable]": "true",
    "columns[1][orderable]": "true",
    "columns[1][search][value]": "",
    "columns[1][search][regex]": "false",
    "columns[2][data]": "cvss",
    "columns[2][name]": "",
    "columns[2][searchable]": "true",
    "columns[2][orderable]": "true",
    "columns[2][search][value]": "",
    "columns[2][search][regex]": "false",
    "columns[3][data]": "cvss3",
    "columns[3][name]": "",
    "columns[3][searchable]": "true",
    "columns[3][orderable]": "true",
    "columns[3][search][value]": "",
    "columns[3][search][regex]": "false",
    "columns[4][data]": "summary",
    "columns[4][name]": "",
    "columns[4][searchable]": "true",
    "columns[4][orderable]": "false",
    "columns[4][search][value]": "",
    "columns[4][search][regex]": "false",
    "columns[5][data]": "last-modified",
    "columns[5][name]": "",
    "columns[5][searchable]": "true",
    "columns[5][orderable]": "true",
    "columns[5][search][value]": "",
    "columns[5][search][regex]": "false",
    "columns[6][data]": "Published",
    "columns[6][name]": "",
    "columns[6][searchable]": "true",
    "columns[6][orderable]": "true",
    "columns[6][search][value]": "",
    "columns[6][search][regex]": "false",
    "order[0][column]": "5",
    "order[0][dir]": "desc",
    "start": "0",
    "length": "50",
    "search[value]": "",
    "search[regex]": "true",
    "retrieve": "cves",
}
def cve_update():
    global data , oldTable , newTable ,newList

    if not os.path.exists("modules/data.txt") :
        _ = open("modules/data.txt", "w+")
        
    num_lines = sum(1 for line in open('modules/data.txt'))

    with open('modules/data.txt' , 'r+') as file :
        oldTable = file.readlines()
    oldTable = [item.strip() for item in oldTable]
    print(oldTable)
    r = requests.post("https://cve.reconshell.com/fetch_cve_data", data=data)
    newTable = [data["id"] for data in r.json()["data"]]

    print(newTable)

    diff = len(set(newTable) - set(oldTable))

    print(diff)

    if len(set(newTable) - set(oldTable)):
        if num_lines != 0 :    
            for index in range(diff):
                print(r.json()["data"][index]["id"])
                embed = discord.Embed(title=f"{r.json()['data'][index]['id']}", description=f"Published : {r.json()['data'][index]['Published']}",color=discord.Color.red())
                embed.add_field(name="summary", value=f"{r.json()['data'][index]['summary'][:600]}")
                embed.add_field(name="CVSS", value=f"{r.json()['data'][index]['cvss']}")
                newList.append(embed)
        with open('modules/data.txt', 'w+') as data_file:
            for item in newTable:
                data_file.writelines(f"{item}\n")
        return newList
    else:
        return None
