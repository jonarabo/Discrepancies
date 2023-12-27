import requests
import json
import tls_client
import re
import csv


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

with open('discreps.csv', 'w', newline='') as csvfile:
    fields = ['Name', 'Stat', 'PP_Line', 'UD_Line', 'Difference']
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()


    pp = requests.get('https://api.prizepicks.com/projections').json()
    ud = requests.get("https://api.underdogfantasy.com/beta/v3/over_under_lines").json()

    pppoints = []
    udpoints = []
    print ("----------------------------------NBA/CBB----------------------------------")
    for x in ud["over_under_lines"]:
        sport = ''.join(x["over_under"]["title"].split()[0:1])
        name = ' '.join(x["over_under"]["title"].split()[0:2])
        stat = f"{x['over_under']['appearance_stat']['display_stat']}"
        value = x['stat_value']
        if stat == 'Points':
            info = {"Name": name.format(), "Stat": stat, "Line": value}
            udpoints.append(info)
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
                pppoints.append(info)
    #print(pplist)



    dict3 = {item["Name"]: float(item["Line"]) for item in pppoints}
    dict4 = {item["Name"]: float(item["Line"]) for item in udpoints}

    common_names = set(dict3.keys()) & set(dict4.keys())

    differences = {name: dict4[name] - dict3[name] for name in common_names}

    pointssorted_differences = sorted(differences.items(), key=lambda x: x[1], reverse=True)

    for name, diff in pointssorted_differences:
        if (diff != 0.0):
            payload = {
                "embeds": [
                    {
                    "description": ("---POINTS---"f"Name: {name}: PP Line: {dict3[name]} UD Line: {dict4[name]} Difference: {diff}"),
                    "color": 5763719,
                    "author": {
                        "name": "ParlayJ"
                        }
                }
            ]
        }
            print("---POINTS---"f"Name: {name}: PP Line: {dict3[name]} UD Line: {dict4[name]} Difference: {diff}")
            requests.post("https://discord.com/api/webhooks/1189173830569173114/_BtRkTJvk03QcAW_hN5w-7vcdxjUzUokbEHVXWsZ3l5D6CUtbxPGITNuPraOAtS7v5cW", json=payload)
            writer.writerow({'Name': name, 'Stat': 'Points', 'PP_Line': dict3.get(name, ''), 'UD_Line': dict4.get(name, ''), 'Difference': diff})


    pprebounds = []
    udrebounds = []

    for x in ud["over_under_lines"]:
        sport = ''.join(x["over_under"]["title"].split()[0:1])
        name = ' '.join(x["over_under"]["title"].split()[0:2])
        stat = f"{x['over_under']['appearance_stat']['display_stat']}"
        value = x['stat_value']
        if stat == 'Rebounds':
            info = {"Name": name.format(), "Stat": stat, "Line": value}
            udrebounds.append(info)
    #print(udlist)

    for x in pp['included']:
        id = x['id']
        name = x['attributes']['name']

        for y in pp['data']:
            did = y['relationships']['new_player']['data']['id']
            value = y['attributes']['line_score']
            stat = y['attributes']['stat_type']
            league = y['relationships']['league']['data']['id']

            if id == did and stat == "Rebounds":
                points = stat == 'Rebounds'
            
            if stat == 'Rebounds' and id == did and int(league) < 50:
                info = {"Name": name.format(), "Stat": stat, "Line": value}
                pprebounds.append(info)
    #print(pplist)


    dict5 = {item["Name"]: float(item["Line"]) for item in pprebounds}
    dict6 = {item["Name"]: float(item["Line"]) for item in udrebounds}

    common_names = set(dict5.keys()) & set(dict6.keys())

    differences = {name: dict6[name] - dict5[name] for name in common_names}

    reboundssorted_differences = sorted(differences.items(), key=lambda x: x[1], reverse=True)

    for name, diff in reboundssorted_differences:
        if (diff != 0.0):
            payload = {
                "embeds": [
                    {
                    "description": ("---REBOUNDS---"f"Name: {name}: PP Line: {dict5[name]} UD Line: {dict6[name]} Difference: {diff}"),
                    "color": 5763719,
                    "author": {
                        "name": "ParlayJ"
                        }
                }
            ]
        }
            print("---REBOUNDS---"f"Name: {name}: PP Line: {dict5[name]} UD Line: {dict6[name]} Difference: {diff}")
            requests.post("https://discord.com/api/webhooks/1189173830569173114/_BtRkTJvk03QcAW_hN5w-7vcdxjUzUokbEHVXWsZ3l5D6CUtbxPGITNuPraOAtS7v5cW", json=payload)
            writer.writerow({'Name': name, 'Stat': 'Rebounds', 'PP_Line': dict5.get(name, ''), 'UD_Line': dict6.get(name, ''), 'Difference': diff})


    ppassists = []
    udassists = []

    for x in ud["over_under_lines"]:
        sport = ''.join(x["over_under"]["title"].split()[0:1])
        name = ' '.join(x["over_under"]["title"].split()[0:2])
        stat = f"{x['over_under']['appearance_stat']['display_stat']}"
        value = x['stat_value']
        if stat == 'Assists':
            info = {"Name": name.format(), "Stat": stat, "Line": value}
            udassists.append(info)
    #print(udlist)

    for x in pp['included']:
        id = x['id']
        name = x['attributes']['name']

        for y in pp['data']:
            did = y['relationships']['new_player']['data']['id']
            value = y['attributes']['line_score']
            stat = y['attributes']['stat_type']
            league = y['relationships']['league']['data']['id']

            if id == did and stat == "Assists":
                points = stat == 'Assists'
            
            if stat == 'Assists' and id == did and int(league) < 50:
                info = {"Name": name.format(), "Stat": stat, "Line": value}
                ppassists.append(info)
    #print(pplist)


    dict7 = {item["Name"]: float(item["Line"]) for item in ppassists}
    dict8 = {item["Name"]: float(item["Line"]) for item in udassists}

    common_names = set(dict7.keys()) & set(dict8.keys())

    differences = {name: dict8[name] - dict7[name] for name in common_names}

    assitssorted_differences = sorted(differences.items(), key=lambda x: x[1], reverse=True)

    for name, diff in assitssorted_differences:
        if (diff != 0.0):
            payload = {
                "embeds": [
                    {
                    "description": ("---ASSISTS---"f"Name: {name}: PP Line: {dict7[name]} UD Line: {dict8[name]} Difference: {diff}"),
                    "color": 5763719,
                    "author": {
                        "name": "ParlayJ"
                        }
                }
            ]
        }
            print("---ASSISTS---"f"Name: {name}: PP Line: {dict7[name]} UD Line: {dict8[name]} Difference: {diff}")
            requests.post("https://discord.com/api/webhooks/1189173830569173114/_BtRkTJvk03QcAW_hN5w-7vcdxjUzUokbEHVXWsZ3l5D6CUtbxPGITNuPraOAtS7v5cW", json=payload)
            writer.writerow({'Name': name, 'Stat': 'Assists', 'PP_Line': dict7.get(name, ''), 'UD_Line': dict8.get(name, ''), 'Difference': diff})


    pppra = []
    udpra = []

    for x in ud["over_under_lines"]:
        sport = ''.join(x["over_under"]["title"].split()[0:1])
        name = ' '.join(x["over_under"]["title"].split()[0:2])
        stat = f"{x['over_under']['appearance_stat']['display_stat']}"
        value = x['stat_value']
        if stat == 'Pts + Rebs + Asts':
            info = {"Name": name.format(), "Stat": stat, "Line": value}
            udpra.append(info)
    #print(udlist)

    for x in pp['included']:
        id = x['id']
        name = x['attributes']['name']

        for y in pp['data']:
            did = y['relationships']['new_player']['data']['id']
            value = y['attributes']['line_score']
            stat = y['attributes']['stat_type']
            league = y['relationships']['league']['data']['id']

            if id == did and stat == "Pts+Rebs+Asts":
                points = stat == 'Pts+Rebs+Asts'
            
            if stat == 'Pts+Rebs+Asts' and id == did and int(league) < 70:
                info = {"Name": name.format(), "Stat": stat, "Line": value}
                pppra.append(info)
    #print(pplist)


    dict9 = {item["Name"]: float(item["Line"]) for item in pppra}
    dict10 = {item["Name"]: float(item["Line"]) for item in udpra}

    common_names = set(dict9.keys()) & set(dict10.keys())

    differences = {name: dict10[name] - dict9[name] for name in common_names}

    prasorted_differences = sorted(differences.items(), key=lambda x: x[1], reverse=True)

    for name, diff in prasorted_differences:
        if (diff != 0.0):
            payload = {
                "embeds": [
                    {
                    "description": ("---PTS+REBS+ASTS---"f"Name: {name}: PP Line: {dict9[name]} UD Line: {dict10[name]} Difference: {diff}"),
                    "color": 5763719,
                    "author": {
                        "name": "ParlayJ"
                        }
                }
            ]
        }
            print("---PTS+REBS+ASTS---"f"Name: {name}: PP Line: {dict9[name]} UD Line: {dict10[name]} Difference: {diff}")
            requests.post("https://discord.com/api/webhooks/1189173830569173114/_BtRkTJvk03QcAW_hN5w-7vcdxjUzUokbEHVXWsZ3l5D6CUtbxPGITNuPraOAtS7v5cW", json=payload)
            writer.writerow({'Name': name, 'Stat': 'Pts+Rebs+Asts', 'PP_Line': dict9.get(name, ''), 'UD_Line': dict10.get(name, ''), 'Difference': diff})


    pppr = []
    udpr = []

    for x in ud["over_under_lines"]:
        sport = ''.join(x["over_under"]["title"].split()[0:1])
        name = ' '.join(x["over_under"]["title"].split()[0:2])
        stat = f"{x['over_under']['appearance_stat']['display_stat']}"
        value = x['stat_value']
        if stat == 'Points + Rebounds':
            info = {"Name": name.format(), "Stat": stat, "Line": value}
            udpr.append(info)
    #print(udlist)

    for x in pp['included']:
        id = x['id']
        name = x['attributes']['name']

        for y in pp['data']:
            did = y['relationships']['new_player']['data']['id']
            value = y['attributes']['line_score']
            stat = y['attributes']['stat_type']
            league = y['relationships']['league']['data']['id']

            if id == did and stat == "Pts+Rebs":
                points = stat == 'Pts+Rebs'
            
            if stat == 'Pts+Rebs' and id == did and int(league) < 70:
                info = {"Name": name.format(), "Stat": stat, "Line": value}
                pppr.append(info)
    #print(pplist)


    dict11 = {item["Name"]: float(item["Line"]) for item in pppr}
    dict12 = {item["Name"]: float(item["Line"]) for item in udpr}

    common_names = set(dict11.keys()) & set(dict12.keys())

    differences = {name: dict12[name] - dict11[name] for name in common_names}

    prsorted_differences = sorted(differences.items(), key=lambda x: x[1], reverse=True)

    for name, diff in prsorted_differences:
        if (diff != 0.0):
            payload = {
                "embeds": [
                    {
                    "description": ("---PTS+REBS---"f"Name: {name}: PP Line: {dict11[name]} UD Line: {dict12[name]} Difference: {diff}"),
                    "color": 5763719,
                    "author": {
                        "name": "ParlayJ"
                        }
                }
            ]
        }
            print("---PTS+REBS---"f"Name: {name}: PP Line: {dict11[name]} UD Line: {dict12[name]} Difference: {diff}")
            requests.post("https://discord.com/api/webhooks/1189173830569173114/_BtRkTJvk03QcAW_hN5w-7vcdxjUzUokbEHVXWsZ3l5D6CUtbxPGITNuPraOAtS7v5cW", json=payload)
            writer.writerow({'Name': name, 'Stat': 'Pts+Rebs', 'PP_Line': dict11.get(name, ''), 'UD_Line': dict12.get(name, ''), 'Difference': diff})

    pppa = []
    udpa = []

    for x in ud["over_under_lines"]:
        sport = ''.join(x["over_under"]["title"].split()[0:1])
        name = ' '.join(x["over_under"]["title"].split()[0:2])
        stat = f"{x['over_under']['appearance_stat']['display_stat']}"
        value = x['stat_value']
        if stat == 'Points + Assists':
            info = {"Name": name.format(), "Stat": stat, "Line": value}
            udpa.append(info)
    #print(udlist)

    for x in pp['included']:
        id = x['id']
        name = x['attributes']['name']

        for y in pp['data']:
            did = y['relationships']['new_player']['data']['id']
            value = y['attributes']['line_score']
            stat = y['attributes']['stat_type']
            league = y['relationships']['league']['data']['id']

            if id == did and stat == "Pts+Asts":
                points = stat == 'Pts+Asts'
            
            if stat == 'Pts+Asts' and id == did and int(league) < 70:
                info = {"Name": name.format(), "Stat": stat, "Line": value}
                pppa.append(info)
    #print(pplist)


    dict13 = {item["Name"]: float(item["Line"]) for item in pppa}
    dict14 = {item["Name"]: float(item["Line"]) for item in udpa}

    common_names = set(dict13.keys()) & set(dict14.keys())

    differences = {name: dict14[name] - dict13[name] for name in common_names}

    pasorted_differences = sorted(differences.items(), key=lambda x: x[1], reverse=True)

    for name, diff in pasorted_differences:
        if (diff != 0.0):
            payload = {
                "embeds": [
                    {
                    "description": ("---PTS+ASTS---"f"Name: {name}: PP Line: {dict13[name]} UD Line: {dict14[name]} Difference: {diff}"),
                    "color": 5763719,
                    "author": {
                        "name": "ParlayJ"
                        }
                }
            ]
        }
            print("---PTS+ASTS---"f"Name: {name}: PP Line: {dict13[name]} UD Line: {dict14[name]} Difference: {diff}")
            requests.post("https://discord.com/api/webhooks/1189173830569173114/_BtRkTJvk03QcAW_hN5w-7vcdxjUzUokbEHVXWsZ3l5D6CUtbxPGITNuPraOAtS7v5cW", json=payload)
            writer.writerow({'Name': name, 'Stat': 'Pts+Asts', 'PP_Line': dict13.get(name, ''), 'UD_Line': dict14.get(name, ''), 'Difference': diff})

    ppra = []
    udra = []

    for x in ud["over_under_lines"]:
        sport = ''.join(x["over_under"]["title"].split()[0:1])
        name = ' '.join(x["over_under"]["title"].split()[0:2])
        stat = f"{x['over_under']['appearance_stat']['display_stat']}"
        value = x['stat_value']
        if stat == 'Rebounds + Assists':
            info = {"Name": name.format(), "Stat": stat, "Line": value}
            udra.append(info)
    #print(udlist)

    for x in pp['included']:
        id = x['id']
        name = x['attributes']['name']

        for y in pp['data']:
            did = y['relationships']['new_player']['data']['id']
            value = y['attributes']['line_score']
            stat = y['attributes']['stat_type']
            league = y['relationships']['league']['data']['id']

            if id == did and stat == "Rebs+Asts":
                points = stat == 'Rebs+Asts'
            
            if stat == 'Rebs+Asts' and id == did and int(league) < 70:
                info = {"Name": name.format(), "Stat": stat, "Line": value}
                ppra.append(info)
    #print(pplist)


    dict15 = {item["Name"]: float(item["Line"]) for item in ppra}
    dict16 = {item["Name"]: float(item["Line"]) for item in udra}

    common_names = set(dict15.keys()) & set(dict16.keys())

    differences = {name: dict16[name] - dict15[name] for name in common_names}

    rasorted_differences = sorted(differences.items(), key=lambda x: x[1], reverse=True)

    for name, diff in rasorted_differences:
        if (diff != 0.0):
            payload = {
                "embeds": [
                    {
                    "description": ("---REBS+ASTS---"f"Name: {name}: PP Line: {dict15[name]} UD Line: {dict16[name]} Difference: {diff}"),
                    "color": 5763719,
                    "author": {
                        "name": "ParlayJ"
                        }
                }
            ]
        }
            print("---REBS+ASTS---"f"Name: {name}: PP Line: {dict15[name]} UD Line: {dict16[name]} Difference: {diff}")
            requests.post("https://discord.com/api/webhooks/1189173830569173114/_BtRkTJvk03QcAW_hN5w-7vcdxjUzUokbEHVXWsZ3l5D6CUtbxPGITNuPraOAtS7v5cW", json=payload)
            writer.writerow({'Name': name, 'Stat': 'Rebs+Asts', 'PP_Line': dict15.get(name, ''), 'UD_Line': dict16.get(name, ''), 'Difference': diff})



    ppbs = []
    udbs = []

    for x in ud["over_under_lines"]:
        sport = ''.join(x["over_under"]["title"].split()[0:1])
        name = ' '.join(x["over_under"]["title"].split()[0:2])
        stat = f"{x['over_under']['appearance_stat']['display_stat']}"
        value = x['stat_value']
        if stat == 'Blocks + Steals':
            info = {"Name": name.format(), "Stat": stat, "Line": value}
            udbs.append(info)
    #print(udlist)

    for x in pp['included']:
        id = x['id']
        name = x['attributes']['name']

        for y in pp['data']:
            did = y['relationships']['new_player']['data']['id']
            value = y['attributes']['line_score']
            stat = y['attributes']['stat_type']
            league = y['relationships']['league']['data']['id']

            if id == did and stat == "Blks+Stls":
                points = stat == 'Blks+Stls'
            
            if stat == 'Blks+Stls' and id == did and int(league) < 70:
                info = {"Name": name.format(), "Stat": stat, "Line": value}
                ppbs.append(info)
    #print(pplist)


    dict17 = {item["Name"]: float(item["Line"]) for item in ppbs}
    dict18 = {item["Name"]: float(item["Line"]) for item in udbs}

    common_names = set(dict17.keys()) & set(dict18.keys())

    differences = {name: dict18[name] - dict17[name] for name in common_names}

    bssorted_differences = sorted(differences.items(), key=lambda x: x[1], reverse=True)

    for name, diff in bssorted_differences:
        if (diff != 0.0):
            payload = {
                "embeds": [
                    {
                    "description": ("---BLKS+STLS---"f"Name: {name}: PP Line: {dict17[name]} UD Line: {dict18[name]} Difference: {diff}"),
                    "color": 5763719,
                    "author": {
                        "name": "ParlayJ"
                        }
                }
            ]
        }
            print("---BLKS+STLS---"f"Name: {name}: PP Line: {dict17[name]} UD Line: {dict18[name]} Difference: {diff}")
            requests.post("https://discord.com/api/webhooks/1189173830569173114/_BtRkTJvk03QcAW_hN5w-7vcdxjUzUokbEHVXWsZ3l5D6CUtbxPGITNuPraOAtS7v5cW", json=payload)
            writer.writerow({'Name': name, 'Stat': 'Blks+Stls', 'PP_Line': dict17.get(name, ''), 'UD_Line': dict18.get(name, ''), 'Difference': diff})

    ppto = []
    udto = []

    for x in ud["over_under_lines"]:
        sport = ''.join(x["over_under"]["title"].split()[0:1])
        name = ' '.join(x["over_under"]["title"].split()[0:2])
        stat = f"{x['over_under']['appearance_stat']['display_stat']}"
        value = x['stat_value']
        if stat == 'Turnovers':
            info = {"Name": name.format(), "Stat": stat, "Line": value}
            udto.append(info)
    #print(udlist)

    for x in pp['included']:
        id = x['id']
        name = x['attributes']['name']

        for y in pp['data']:
            did = y['relationships']['new_player']['data']['id']
            value = y['attributes']['line_score']
            stat = y['attributes']['stat_type']
            league = y['relationships']['league']['data']['id']

            if id == did and stat == "Turnovers":
                points = stat == 'Turnovers'
            
            if stat == 'Turnovers' and id == did and int(league) < 70:
                info = {"Name": name.format(), "Stat": stat, "Line": value}
                ppto.append(info)
    #print(pplist)


    dict19 = {item["Name"]: float(item["Line"]) for item in ppto}
    dict20 = {item["Name"]: float(item["Line"]) for item in udto}

    common_names = set(dict19.keys()) & set(dict20.keys())

    differences = {name: dict20[name] - dict19[name] for name in common_names}

    tosorted_differences = sorted(differences.items(), key=lambda x: x[1], reverse=True)

    for name, diff in tosorted_differences:
        if (diff != 0.0):
            payload = {
                "embeds": [
                    {
                    "description": ("---TURNOVERS---"f"Name: {name}: PP Line: {dict19[name]} UD Line: {dict20[name]} Difference: {diff}"),
                    "color": 5763719,
                    "author": {
                        "name": "ParlayJ"
                        }
                }
            ]
        }
            print("---TURNOVERS---"f"Name: {name}: PP Line: {dict19[name]} UD Line: {dict20[name]} Difference: {diff}")
            requests.post("https://discord.com/api/webhooks/1189173830569173114/_BtRkTJvk03QcAW_hN5w-7vcdxjUzUokbEHVXWsZ3l5D6CUtbxPGITNuPraOAtS7v5cW", json=payload)
            writer.writerow({'Name': name, 'Stat': 'Turnovers', 'PP_Line': dict19.get(name, ''), 'UD_Line': dict20.get(name, ''), 'Difference': diff})

    
print ("----------------------------------CS2----------------------------------")

ppkills = []
udkills = []

for x in ud["over_under_lines"]:
    sport = ''.join(x["over_under"]["title"].split()[0:1])
    name = ' '.join(x["over_under"]["title"].split()[0:2])
    stat = f"{x['over_under']['appearance_stat']['display_stat']}"
    value = x['stat_value']
    if stat == 'Kills on Map 1+2':
        name = name.replace("CS: ", "").strip()
        info = {"Name": name.format(), "Stat": stat, "Line": value}
        udkills.append(info)
#print(udkills)

for x in pp['included']:
    id = x['id']
    name = x['attributes']['name']

    for y in pp['data']:
        did = y['relationships']['new_player']['data']['id']
        value = y['attributes']['line_score']
        stat = y['attributes']['stat_type']
        league = y['relationships']['league']['data']['id']

        if id == did and stat == "MAPS 1-2 Kills":
            points = stat == 'MAPS 1-2 Kills'
        
        if stat == 'MAPS 1-2 Kills' and id == did:
            info = {"Name": name.format(), "Stat": stat, "Line": value}
            ppkills.append(info)
#print(ppkills)

dict21 = {item["Name"]: float(item["Line"]) for item in ppkills}
dict22 = {item["Name"]: float(item["Line"]) for item in udkills}

common_names = set(dict21.keys()) & set(dict22.keys())

differences = {name: dict22[name] - dict21[name] for name in common_names}

killssorted_differences = sorted(differences.items(), key=lambda x: x[1], reverse=True)

for name, diff in killssorted_differences:
    if diff != 0.0:
        print("---MAP1+2KILLS---"f"Name: {name}: PP Line: {dict21[name]} UD Line: {dict22[name]} Difference: {diff}")
        #writer.writerow({'Name': name, 'Stat': 'MAP1+2KILLS', 'PP_Line': dict21.get(name, ''), 'UD_Line': dict22.get(name, ''), 'Difference': diff})


pphs = []
udhs = []

for x in ud["over_under_lines"]:
    sport = ''.join(x["over_under"]["title"].split()[0:1])
    name = ' '.join(x["over_under"]["title"].split()[0:2])
    stat = f"{x['over_under']['appearance_stat']['display_stat']}"
    value = x['stat_value']
    if stat == 'Headshots on Maps 1+2':
        name = name.replace("CS: ", "").strip()
        info = {"Name": name.format(), "Stat": stat, "Line": value}
        udhs.append(info)
#print(udkills)

for x in pp['included']:
    id = x['id']
    name = x['attributes']['name']

    for y in pp['data']:
        did = y['relationships']['new_player']['data']['id']
        value = y['attributes']['line_score']
        stat = y['attributes']['stat_type']
        league = y['relationships']['league']['data']['id']

        if id == did and stat == "MAPS 1-2 Headshots":
            points = stat == 'MAPS 1-2 Headshots'
        
        if stat == 'MAPS 1-2 Headshots' and id == did:
            info = {"Name": name.format(), "Stat": stat, "Line": value}
            pphs.append(info)
#print(ppkills)

dict25 = {item["Name"]: float(item["Line"]) for item in pphs}
dict26 = {item["Name"]: float(item["Line"]) for item in udhs}

common_names = set(dict25.keys()) & set(dict26.keys())

differences = {name: dict26[name] - dict25[name] for name in common_names}

hsssorted_differences = sorted(differences.items(), key=lambda x: x[1], reverse=True)

for name, diff in hsssorted_differences:
    if diff != 0.0:
        print("---MAP1+2Headshots---"f"Name: {name}: PP Line: {dict25[name]} UD Line: {dict26[name]} Difference: {diff}")
        #writer.writerow({'Name': name, 'Stat': 'MAP1+2KILLS', 'PP_Line': dict21.get(name, ''), 'UD_Line': dict22.get(name, ''), 'Difference': diff})



print ("----------------------------------LOL----------------------------------")

pplol = []
udlol = []

for x in ud["over_under_lines"]:
    sport = ''.join(x["over_under"]["title"].split()[0:1])
    name = ' '.join(x["over_under"]["title"].split()[0:2])
    stat = f"{x['over_under']['appearance_stat']['display_stat']}"
    value = x['stat_value']
    if stat == 'Kills in Map 1':
        name = name.replace("LoL: ", "").strip()
        info = {"Name": name.format(), "Stat": stat, "Line": value}
        udlol.append(info)
#print(udlol)

for x in pp['included']:
    id = x['id']
    name = x['attributes']['name']

    for y in pp['data']:
        did = y['relationships']['new_player']['data']['id']
        value = y['attributes']['line_score']
        stat = y['relationships']['league']['data']['type'] #find better way to index stats for league
        league = y['relationships']['league']['data']['id']

        if id == did and stat == "league":
            points = stat == 'league'
        
        if stat == 'league' and id == did:
            info = {"Name": name.format(), "Stat": stat, "Line": value}
            pplol.append(info)
#print(pplol)

dict23 = {item["Name"]: float(item["Line"]) for item in pplol}
dict24 = {item["Name"]: float(item["Line"]) for item in udlol}

common_names = set(dict23.keys()) & set(dict24.keys())

differences = {name: dict24[name] - dict23[name] for name in common_names}

lolsorted_differences = sorted(differences.items(), key=lambda x: x[1], reverse=True)

for name, diff in lolsorted_differences:
    if diff != 0.0:
        print("---MAP1KILLS---"f"Name: {name}: PP Line: {dict23[name]} UD Line: {dict24[name]} Difference: {diff}")
        #writer.writerow({'Name': name, 'Stat': 'MAP1KILLS', 'PP_Line': dict23.get(name, ''), 'UD_Line': dict24.get(name, ''), 'Difference': diff})
