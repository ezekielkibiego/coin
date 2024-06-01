import json
import requests
from datetime import datetime
from decouple import config

# Replace with your actual CoinMarketCap API key
api_key = config("COIN_API_KEY")
currency = 'KES'
global_url = f'https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest?convert={currency}'
listings_url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?convert={currency}'

# Define headers including the API key
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': api_key,
}

# Function to fetch global metrics
def fetch_global_metrics():
    response = requests.get(global_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed to retrieve global metrics: {response.status_code} - {response.text}')
        return None

# Function to fetch cryptocurrency listings
def fetch_cryptocurrency_listings():
    response = requests.get(listings_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed to retrieve cryptocurrency listings: {response.status_code} - {response.text}')
        return None

# Fetch global metrics data
global_results = fetch_global_metrics()

if global_results:
    # Extract the relevant data from the JSON response
    try:
        active_cryptocurrencies = global_results['data']['active_cryptocurrencies']
        active_markets = global_results['data']['active_exchanges']
        bitcoin_percentage = global_results['data']['btc_dominance']
        last_updated = global_results['status']['timestamp']
        global_cap = global_results['data']['quote'][currency]['total_market_cap']
        global_volume = global_results['data']['quote'][currency]['total_volume_24h']

        # Format the numbers with commas
        active_cryptocurrencies_string = '{:,}'.format(active_cryptocurrencies)
        active_markets_string = '{:,}'.format(active_markets)
        global_cap_string = '{:,}'.format(int(global_cap))
        global_volume_string = '{:,}'.format(int(global_volume))

        # Format the last updated time
        last_updated_string = datetime.strptime(last_updated, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%B %d, %Y at %I:%M %p')

        print()
        print(f'There are currently {active_cryptocurrencies_string} active cryptocurrencies and {active_markets_string} active markets.')
        print(f'The global cap of all cryptos is {global_cap_string} KES and 24h global volume is {global_volume_string} KES.')
        print(f'Bitcoin\'s total percentage of the global cap is {bitcoin_percentage}%.')
        print()
        print(f'This information was updated on {last_updated_string}.')
    except KeyError as e:
        print(f'Error: Missing key in response data - {e}')

# Fetch cryptocurrency listings data
listings_results = fetch_cryptocurrency_listings()

if listings_results:
    # Extract the relevant data from the JSON response
    try:
        cryptocurrencies = listings_results['data']

        # Print header
        print(f"\n{'Name':<20} {'Symbol':<10} {'Price (KES)':>15}")

        # Iterate over the list of cryptocurrencies and print their details
        for crypto in cryptocurrencies:
            name = crypto['name']
            symbol = crypto['symbol']
            price = crypto['quote'][currency]['price']
            print(f"{name:<20} {symbol:<10} {price:>15,.2f} KES")

    except KeyError as e:
        print(f'Error: Missing key in response data - {e}')