'''
Module for adding features
'''
import requests
import discord
import os







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
