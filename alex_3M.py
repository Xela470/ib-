import requests
from tradingview_screener import Column, Query
import numpy as np
import json
import pandas as pd
from datetime import datetime, date, timedelta

import datetime

# Get screener data
n_rows, df = Query().select(
    'name','exchange','close','volume','Perf.3M','average_volume_90d_calc',
    'average_volume_60d_calc','ADR','SMA50','SMA200'
).where(    
    Column('Perf.3M') > 50, 
    Column('average_volume_90d_calc') > 500000, 
    Column('close') >= 1,
    Column('exchange') != 'OTC'
).order_by('Perf.3M', ascending=False).get_scanner_data()

# Ajouter la nouvelle colonne 'adr_%'
df['adr_%'] = df['ADR'] / df['close']*100

# Appliquer tous les filtres en une seule étape
df_final = df[
    (df['adr_%'] >= 7)
].copy()



# Récupérer les nouvelles et les profils pour tous les symboles dans df_final
symbols = df_final['name'].tolist()


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, float):
            if np.isnan(obj):
                return None
            if np.isinf(obj):
                return None if obj < 0 else 'Infinity'
        return super().default(obj)


# Format the data for Pabbly/Notion and handle NaN values
formatted_data = df_final.replace({np.nan: None, np.inf: None, -np.inf: None}).to_dict(orient='records')

json_data = json.dumps({"data": formatted_data}, cls=CustomJSONEncoder)

# def send_to_pabbly(data):
#     webhook_url = "https://connect.pabbly.com/workflow/sendwebhookdata/IjU3NjYwNTZmMDYzMTA0M2M1MjZlNTUzYzUxMzEi_pc"
#     response = requests.post(webhook_url, json=data)
#     return response.status_code

# status = send_to_pabbly(json.loads(json_data))
# print(f"Status: {status}")

# Afficher le résultat
print(df_final)

# Replace with your session ID
session_id = "ree3t1ozq9cco27vi50dvvlg94evznvm"
watchlist_id = "174683773"

# Base URL for the API
base_url = "https://www.tradingview.com/api/v1/symbols_list/custom"

# Common headers used for requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:134.0) Gecko/20100101 Firefox/134.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://www.tradingview.com/',
    'Content-Type': 'application/json',
    'x-language': 'en',
    'x-requested-with': 'XMLHttpRequest',
    'Origin': 'https://www.tradingview.com',
    'DNT': '1',
}

# Cookies
cookies = {
    'sessionid': session_id,
}

# Function to fetch the watchlist
def fetch_watchlist(watchlist_id):
    url = f"{base_url}/{watchlist_id}"
    response = requests.get(url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        try:
            data = response.json()
            print("Watchlist Symbols:", data.get("symbols", []))
        except ValueError:
            print("Error: Response is not in JSON format.")
    else:
        print(f"Error: Received status code {response.status_code}")
        print(response.text)

# Function to clear the watchlist
def clear_watchlist(watchlist_id):
    url = f"{base_url}/{watchlist_id}/replace/?unsafe=true"
    payload = []  # Empty payload to clear the watchlist
    response = requests.post(url, headers=headers, cookies=cookies, json=payload)
    if response.status_code == 200:
        print("Watchlist cleared successfully.")
    else:
        print(f"Error: Unable to clear the watchlist. Status code {response.status_code}")
        print(response.text)

# Function to add symbols to the watchlist
def add_symbols_to_watchlist(watchlist_id, symbols):
    url = f"{base_url}/{watchlist_id}/append/"
    payload = symbols  # List of symbols to add
    response = requests.post(url, headers=headers, cookies=cookies, json=payload)
    if response.status_code == 200:
        print(f"Symbols {symbols} added successfully to the watchlist.")
    else:
        print(f"Error: Unable to add symbols to the watchlist. Status code {response.status_code}")
        print(response.text)


# Example usage
if __name__ == "__main__":
    # Fetch the current watchlist
    print("Fetching watchlist...")
    fetch_watchlist(watchlist_id)

    # Clear the watchlist
    print("\nClearing watchlist...")
    clear_watchlist(watchlist_id)

    # Add symbols to the watchlist
    symbols_to_add = [symbol for symbol in symbols]

    print("\nAdding symbols to watchlist...")
    add_symbols_to_watchlist(watchlist_id, symbols_to_add)
   
    # Verify that the symbols were added
    print("\nFetching watchlist again to verify...")
    fetch_watchlist(watchlist_id)
