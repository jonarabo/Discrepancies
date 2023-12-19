import requests
import urllib
from datetime import datetime, timedelta

BASE_URL = 'https://api.prop-odds.com'
API_KEY = 'KUJ9DafGwXoI5wowMOlliun1qaxOqBfssErPE97p1as'

def get_request(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()

    print('Request failed with status:', response.status_code)
    return {}

from datetime import datetime, timedelta

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

    # Filter markets based on the market name or another relevant field
    filtered_markets = [market for market in markets.get('markets', []) if market.get('name') == market_type]
    return {'markets': filtered_markets}

def get_most_recent_odds(game_id, market, sportsbooks=['fanduel','draftkings']):
    query_params = {
        'api_key': API_KEY,
    }
    params = urllib.parse.urlencode(query_params)
    url = BASE_URL + '/beta/odds/' + game_id + '/' + market + '?' + params
    odds = get_request(url)

    # Filter odds based on the desired sportsbooks and exclude alternate points lines
    filtered_odds = {}
    if 'sportsbooks' in odds:
        for sportsbook_data in odds['sportsbooks']:
            bookie_key = sportsbook_data.get('bookie_key', '').lower()
            if bookie_key in sportsbooks:
                market_data = sportsbook_data.get('market', {})
                outcomes = market_data.get('outcomes', [])

                # Exclude alternate points lines based on the 'description' field
                filtered_outcomes = [outcome for outcome in outcomes if 'Alt Points' not in outcome.get('description', '')]

                filtered_odds[bookie_key] = filtered_outcomes

    return {'odds': filtered_odds}

def main():
# Get the current date
    today = datetime.now()

    # Get the date for the next day
    next_day = today + timedelta(days=0)

    # Get NBA games for the next day
    games = get_nba_games_for_date(next_day)

    if len(games['games']) == 0:
        print(f'No NBA games scheduled for {next_day.strftime("%Y-%m-%d")}.')
        return

    # Filter games based on the desired time range (adjust as needed)
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
    print(odds)

if __name__ == '__main__':
    main()
