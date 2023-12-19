import requests
import urllib
from datetime import datetime, timedelta
import tls_client

BASE_URL = 'https://api.prop-odds.com'
API_KEY = 'KUJ9DafGwXoI5wowMOlliun1qaxOqBfssErPE97p1as'

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

def get_nba_games_for_date(target_date):
    query_params = {
        'date': target_date.strftime('%Y-%m-%d'),
        'tz': 'America/New_York',
        'api_key': API_KEY,
    }
    params = urllib.parse.urlencode(query_params)
    url = BASE_URL + '/beta/games/nba?' + params
    return get_request(url)

def filter_games_by_time(games, start_time, end_time):
    filtered_games = [game for game in games['games'] if start_time <= game.get('start_time', '') <= end_time]
    return {'games': filtered_games}

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

def get_most_recent_odds(game_id, market, sportsbooks=['fanduel','draftkings']):
    query_params = {
        'api_key': API_KEY,
    }
    params = urllib.parse.urlencode(query_params)
    url = BASE_URL + '/beta/odds/' + game_id + '/' + market + '?' + params
    odds = get_request(url)

    filtered_odds = {}
    if 'sportsbooks' in odds:
        for sportsbook_data in odds['sportsbooks']:
            bookie_key = sportsbook_data.get('bookie_key', '').lower()
            if bookie_key in sportsbooks:
                market_data = sportsbook_data.get('market', {})
                outcomes = market_data.get('outcomes', [])
                filtered_outcomes = [outcome for outcome in outcomes if 'Alt Points' not in outcome.get('description', '')]
                filtered_odds[bookie_key] = filtered_outcomes

    return {'odds': filtered_odds}

oddslist = {}

def main():

    today = datetime.now()

    next_day = today + timedelta(days=0)

    games = get_nba_games_for_date(next_day)

    if len(games['games']) == 0:
        print(f'No NBA games scheduled for {next_day.strftime("%Y-%m-%d")}.')
        return

    start_time = next_day.strftime('%Y-%m-%dT00:00:00')
    end_time = next_day.strftime('%Y-%m-%dT23:59:59')
    filtered_games = filter_games_by_time(games, start_time, end_time)

    first_game = games['games'][0]
    game_id = first_game['game_id']
    game_info = get_game_info(game_id)

    markets = get_markets(game_id)
    if len(markets['markets']) == 0:
        print('No markets found.')
        return

    first_market = markets['markets'][0]
    odds = get_most_recent_odds(game_id, first_market['name'], sportsbooks=['fanduel','draftkings'])
    oddslist.update(odds)
    #print(oddslist)
    #print(oddslist.keys())

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

fdlist = []

for entry in oddslist.get('odds', {}).get('fanduel', []):
    name = entry.get('participant_name', '')
    handicap = entry.get('handicap', '')
    odds = entry.get('odds', '')
    odds_info = {"Name": name, "Stat": handicap, "Line": odds}
    fdlist.append(odds_info)

print(fdlist)




dict3 = {item["Name"]: float(item["Line"]) for item in pplist}
dict4 = {item["Name"]: float(item["Line"]) for item in udlist}
dict5 = {item["Name"]: float(item["Line"]) for item in oddslist}


common_names = set(dict3.keys()) & set(dict4.keys()) & set(dict5.keys())

differences = {name: dict4[name] - dict3[name] for name in common_names}

sorted_differences = sorted(differences.items(), key=lambda x: x[1], reverse=True)
''''
for name, diff in sorted_differences:
    if (diff != 0.0):
        print(f"Name: {name}: PP Line: {dict3[name]} UD Line: {dict4[name]} Difference: {diff}")
'''

if __name__ == '__main__':
    main()
