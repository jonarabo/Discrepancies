import requests
import json
import tls_client
import re


headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}

requests = tls_client.Session(
    client_identifier="chrome112",
)

pp = requests.get('https://api.prizepicks.com/projections').json()
ud = requests.get("https://api.underdogfantasy.com/beta/v3/over_under_lines").json()

pplist = []
udlist = []
combinedlist = []

for x in ud["over_under_lines"]:
    sport = ''.join(x["over_under"]["title"].split()[0:1])
    name = ' '.join(x["over_under"]["title"].split()[0:2])
    stat = f"{x['over_under']['appearance_stat']['display_stat']}"
    value = x['stat_value']
    if stat == 'Points':
        info = {"Name": name.format(), "Stat": stat, "Line": value}
        udlist.append(info)
#print(udlist)

for x in pp['included']:
    id = x['id']
    name = x['attributes']['name']

    for y in pp['data']:
        did = y['relationships']['new_player']['data']['id']
        value = y['attributes']['line_score']
        stat = y['attributes']['stat_type']
        league = y['relationships']['league']['data']['id']

        if id == did and stat == "Points":
            points = stat == 'Points'
        
        if stat == 'Points' and id == did and int(league) < 50:
            info = {"Name": name.format(), "Stat": stat, "Line": value}
            pplist.append(info)
#print(pplist)



dict3 = {item["Name"]: float(item["Line"]) for item in pplist}
dict4 = {item["Name"]: float(item["Line"]) for item in udlist}

common_names = set(dict3.keys()) & set(dict4.keys())

differences = {name: dict4[name] - dict3[name] for name in common_names}

sorted_differences = sorted(differences.items(), key=lambda x: x[1], reverse=True)

for name, diff in sorted_differences:
    if (diff != 0.0):
        print(f"Name: {name}: PP Line: {dict3[name]} UD Line: {dict4[name]} Difference: {diff}")
