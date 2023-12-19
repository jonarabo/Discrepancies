data = {
    'odds': {
        'fanduel': [
            {
                'timestamp': '2023-12-19T08:20:03',
                'handicap': 22.5,
                'odds': -104,
                'participant': 16150,
                'participant_name': 'Brandon Ingram',
                'name': 'Brandon Ingram Over',
                'description': 'Brandon Ingram - Points'
            }
        ]
    }
}

# Accessing the information
name = data['odds']['fanduel'][0]['participant_name']
odds = data['odds']['fanduel'][0]['odds']
handicap = data['odds']['fanduel'][0]['handicap']

# Printing the results
print(f"Name: {name}")
print(f"Odds: {odds}")
print(f"Handicap: {handicap}")
