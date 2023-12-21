import requests
import urllib
from datetime import datetime, timedelta
import tls_client
import json

BASE_URL = 'https://api.prop-odds.com'
API_KEY = 'tUyC39x5rploU3BFK0lylig2jeVtfBEdAH4Tupxdfc'

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


def get_request(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()

    print('Request failed with status:', response.status_code)
    return {}


def get_nba_games():
    ''' 
    now = datetime.now()
    tomorrow = now + timedelta(days=1)
    query_params = {
        'date': tomorrow.strftime('%Y-%m-%d'),
        'tz': 'America/New_York',
        'api_key': API_KEY,
    }
    # Comment out below code to show games for today, comment out above code to show games for tomorrow 
    ''' 
    now = datetime.now()
    query_params = {
        'date': now.strftime('%Y-%m-%d'),
        'tz': 'America/New_York',
        'api_key': API_KEY,
    }
    




    params = urllib.parse.urlencode(query_params)
    url = BASE_URL + '/beta/games/nba?' + params
    return get_request(url)

def get_game_info(game_id):
    query_params = {
        'api_key': API_KEY,
    }
    params = urllib.parse.urlencode(query_params)
    url = BASE_URL + '/beta/game/' + game_id + '?' + params
    return get_request(url)


def get_markets(game_id, market_type='player_points_over_under'):
    query_params = {
        'api_key': API_KEY,
    }
    params = urllib.parse.urlencode(query_params)
    url = BASE_URL + '/beta/markets/' + game_id + '?' + params
    markets = get_request(url)

    filtered_markets = [market for market in markets.get('markets', []) if market.get('name') == market_type]
    return {'markets': filtered_markets}


def get_most_recent_odds(game_id, market):
    query_params = {
        'api_key': API_KEY,
    }
    params = urllib.parse.urlencode(query_params)
    url = BASE_URL + '/beta/odds/' + game_id + '/' + market + '?' + params
    odds_response = get_request(url)

    if 'sportsbooks' in odds_response:
        for bookie in odds_response['sportsbooks']:
            bookie['market']['outcomes'] = [
                outcome for outcome in bookie['market'].get('outcomes', [])
                if 'Alt' not in outcome.get('description', '')
            ]

    return odds_response

oddslist = []

def extract_odds_information(odds):
    for bookie in odds.get('sportsbooks', []):
        market = bookie.get('market', {})
        outcomes = market.get('outcomes', [])
        for outcome in outcomes:
            participant_name = outcome.get('participant_name')
            handicap = outcome.get('handicap')
            odds_value = outcome.get('odds')

            if participant_name is not None and handicap is not None and odds_value is not None:
                odds_info = {"Name": participant_name, "Line": handicap, "Odds": odds_value}
                oddslist.append(odds_info)
                #print(oddslist)

                # Check if the participant_name and handicap exist in pplist or udlist
                #if any(player['Name'] == participant_name and player['Line'] == handicap for player in pplist + udlist):
                #    print(f"Name: {participant_name}, Line: {handicap}, Odds: {odds_value}")

                


def main():

    games = get_nba_games()
    if len(games['games']) == 0:
        print('No games scheduled for today.')
        return

    for game in games['games']:
        game_id = game['game_id']
        #print(f"\nGame ID: {game_id}")
        
        # Get game info
        game_info = get_game_info(game_id)
        # Print relevant game information if needed
        
        # Get all markets for the game
        markets = get_markets(game_id)
        if len(markets['markets']) == 0:
            print('No markets found for this game.')
            continue

        for market in markets['markets']:
            market_name = market['name']
            #print(f"\nMarket: {market_name}")
            
            # Get odds for the market
            odds = get_most_recent_odds(game_id, market_name)
            extract_odds_information(odds)
            
            #oddslist.append(odds)
            #with open('oddslist.json', 'w') as json_file:
                #json.dump(oddslist, json_file, indent=2)
            #print(oddslist)
            #print(odds)

pp = requests.get('https://api.prizepicks.com/projections').json()
ud = requests.get("https://api.underdogfantasy.com/beta/v3/over_under_lines").json()

pplist = []
udlist = []

for x in ud["over_under_lines"]:
    sport = ''.join(x["over_under"]["title"].split()[0:1])
    name = ' '.join(x["over_under"]["title"].split()[0:2])
    stat = f"{x['over_under']['appearance_stat']['display_stat']}"
    value = x['stat_value']
    if stat == 'Points':
        odds_info = {"Name": name.format(), "Stat": stat, "Line": value}
        udlist.append(odds_info)
#print(udlist)

for x in pp['included']:
    id = x['id']
    name = x['attributes']['name']

    for y in pp['data']:
        did = y['relationships']['new_player']['data']['id']
        value = y['attributes']['line_score']
        stat = y['attributes']['stat_type']
        league = y['relationships']['league']['data']['id']

        if stat == 'Points' and id == did and int(league) < 50:
            odds_info = {"Name": name.format(), "Stat": stat, "Line": value}
            pplist.append(odds_info)
#print(pplist)

dict3 = {item["Name"]: float(item["Line"]) for item in pplist}
dict4 = {item["Name"]: float(item["Line"]) for item in udlist}
#dict5 = {item["Name"]: float(item["Line"]) for item in oddslist}


common_names = set(dict3.keys()) & set(dict4.keys()) #& set(dict5.keys())

differences = {name: dict4[name] - dict3[name] for name in common_names}

sorted_differences = sorted(differences.items(), key=lambda x: x[1], reverse=True)

for name, diff in sorted_differences:
        if diff != 0.0:
            print(f"Name: {name}, PP Line: {dict3[name]}, UD Line: {dict4[name]}, Difference: {diff}, Fanduel Odds: ")



if __name__ == '__main__':
    main()
