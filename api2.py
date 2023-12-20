import requests
import urllib
from datetime import datetime

BASE_URL = 'https://api.prop-odds.com'
API_KEY = 'KUJ9DafGwXoI5wowMOlliun1qaxOqBfssErPE97p1as'


def get_request(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()

    print('Request failed with status:', response.status_code)
    return {}


def get_nba_games():
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
            print(odds)


if __name__ == '__main__':
    main()
