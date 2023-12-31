import requests
import urllib
from datetime import datetime, timedelta
import tls_client


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


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

requests = tls_client.Session(
    client_identifier="chrome112",
)

# Functions

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

def get_markets(game_id, market_types):
    query_params = {
        'api_key': API_KEY,
    }
    params = urllib.parse.urlencode(query_params)
    
    markets_data = []
    
    for market_type in market_types:
        url = BASE_URL + '/beta/markets/' + game_id + '?' + params
        markets = get_request(url)
        
        filtered_markets = [market for market in markets.get('markets', []) if market.get('name') == market_type]
        markets_data.extend(filtered_markets)
    
    return {'markets': markets_data}

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

oddslist = []  # Assuming you want to store Fanduel odds for each participant

def extract_odds_information(odds):
    name_count = {}  # Keep track of the count for each name
    for bookie in odds.get('sportsbooks', []):
        market = bookie.get('market', {})
        outcomes = market.get('outcomes', [])
        for outcome in outcomes:
            participant_name = outcome.get('participant_name')
            handicap = outcome.get('handicap')
            odds_value = outcome.get('odds')

            if participant_name is not None and handicap is not None and odds_value is not None:
                count = name_count.get(participant_name, 0)
                if count < 2:
                    odds_info = {"Name": participant_name, "Line": handicap, "Odds": odds_value}
                    oddslist.append(odds_info)
                    name_count[participant_name] = count + 1

# Main function

def main():
    games = get_nba_games()
    if len(games['games']) == 0:
        print('No games scheduled for today.')
        return

    for game in games['games']:
        game_id = game['game_id']
        game_info = get_game_info(game_id)

        market_types = ['player_points_over_under', 'player_rebounds_over_under']
        markets = get_markets(game_id, market_types)
        
        if len(markets['markets']) == 0:
            # print('No markets found for this game.')
            continue

        for market in markets['markets']:
            market_name = market['name']
            odds_info = get_most_recent_odds(game_id, market_name)
            extract_odds_information(odds_info)

            #print(f"\nGame ID: {game_id}, Market: {market_name}")

    for odds_dict in oddslist:
        odds_name = odds_dict['Name']
        if odds_name in common_names:
            pp_line_points = dict3.get(odds_name, None)
            ud_line_points = dict4.get(odds_name, None)
            diffpoints = ud_line_points - pp_line_points
            if diffpoints != 0.0:
                print(color.RED + 'POINTS' + color.END + f"Name: {odds_name}, PP Line: {pp_line_points}, UD Line: {ud_line_points}, Difference: {diffpoints}, Fanduel Line: {odds_dict.get('Line', None)}, Fanduel Odds: {odds_dict.get('Odds', None)}")

    for odds_dict in oddslist:
        odds_name = odds_dict['Name']
        if odds_name in common_names:
            pp_line_rebounds = dict5.get(odds_name, None)
            ud_line_rebounds = dict6.get(odds_name, None)
            diffreb = ud_line_rebounds - pp_line_rebounds
            if diffreb != 0.0:
                print(color.BLUE + 'REBOUNDS' + color.END + f"Name: {odds_name}, PP Line: {pp_line_rebounds}, UD Line: {ud_line_rebounds}, Difference: {diffreb}, Fanduel Line: {odds_dict.get('Line', None)}, Fanduel Odds: {odds_dict.get('Odds', None)}")

if __name__ == '__main__':
    main()
