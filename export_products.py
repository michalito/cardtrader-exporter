import os
import requests
import pandas as pd
from datetime import datetime

# Get the API token from the environment variable
API_TOKEN = os.getenv('API_TOKEN')

if not API_TOKEN:
    raise ValueError("No API token provided. Set the API_TOKEN environment variable.")

# Define the endpoint URLs
products_url = "https://api.cardtrader.com/api/v2/products/export"
expansions_url = "https://api.cardtrader.com/api/v2/expansions/export"

# Set the headers including the authorization token
headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

# Function to make GET requests and return JSON response
def get_api_data(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
        print(response.text)
        return []

# Fetch products and expansions data
products = get_api_data(products_url, headers)
expansions = get_api_data(expansions_url, headers)

# Convert JSON data to pandas DataFrames
df_products = pd.DataFrame(products)
df_expansions = pd.DataFrame(expansions)

# Extract expansion_id from the 'expansion' column in the products DataFrame
if 'expansion' in df_products.columns:
    df_products['expansion_id'] = df_products['expansion'].apply(lambda x: x['id'] if isinstance(x, dict) and 'id' in x else None)

# Rename the 'name_en' column to 'name' in products DataFrame
if 'name_en' in df_products.columns:
    df_products.rename(columns={'name_en': 'name'}, inplace=True)

# Merge expansions data to products data
if 'expansion_id' in df_products.columns and 'id' in df_expansions.columns:
    df_expansions.rename(columns={'id': 'expansion_id', 'name': 'expansion_name'}, inplace=True)
    df_products = df_products.merge(df_expansions[['expansion_id', 'expansion_name']], on='expansion_id', how='left')

# Transform price from cents to euros in products DataFrame
if 'price_cents' in df_products.columns:
    df_products['price_eur'] = df_products['price_cents'] / 100

# Define the game_id to game name mapping
game_id_mapping = {
    1: "Magic: The Gathering",
    5: "Pokemon",
    6: "Flesh And Blood",
    18: "Lorcana",
    20: "Star Wars Unlimited"
}

# Add the game_name column based on game_id mapping
if 'game_id' in df_products.columns:
    df_products['game_name'] = df_products['game_id'].map(game_id_mapping)

# Expand the 'properties_hash' column into separate columns
if 'properties_hash' in df_products.columns:
    properties_df = pd.json_normalize(df_products['properties_hash'])
    df_products = df_products.drop('properties_hash', axis=1).join(properties_df)

# Columns to be removed from game-specific exports
columns_to_remove = [
    'uploaded_images', 'price_cents', 'blueprint_id', 'expansion', 'category_id', 'user_id', 
    'id', 'tag', 'bundle_size', 'user_data_field', 'game_id', 'expansion_id'
]

# Prefixes to check for removal in game-specific exports
prefixes_to_check = {
    1: ['pokemon', 'fab', 'starwars', 'lorcana'],  # Remove these prefixes from Magic: The Gathering export
    5: ['mtg', 'fab', 'starwars', 'lorcana'],      # Remove these prefixes from Pokemon export
    6: ['mtg', 'pokemon', 'starwars', 'lorcana'],  # Remove these prefixes from Flesh And Blood export
    18: ['mtg', 'pokemon', 'fab', 'starwars'],     # Remove these prefixes from Lorcana export
    20: ['mtg', 'pokemon', 'fab', 'lorcana']       # Remove these prefixes from Star Wars Unlimited export
}

# Get today's date and format it as a string
today_date = datetime.now().strftime("%Y-%m-%d")

# Create the exports directory if it doesn't exist
exports_dir = "exports"
os.makedirs(exports_dir, exist_ok=True)

# Create the CSV file names with the current date
products_file_name = os.path.join(exports_dir, f"products_{today_date}.csv")
expansions_file_name = os.path.join(exports_dir, f"expansions_{today_date}.csv")

# Export DataFrames to CSV
df_products.to_csv(products_file_name, index=False)
df_expansions.to_csv(expansions_file_name, index=False)

# Export a file per game
game_files_mapping = {
    1: os.path.join(exports_dir, f"products_mtg_{today_date}.csv"),
    5: os.path.join(exports_dir, f"products_pokemon_{today_date}.csv"),
    6: os.path.join(exports_dir, f"products_fab_{today_date}.csv"),
    18: os.path.join(exports_dir, f"products_lorcana_{today_date}.csv"),
    20: os.path.join(exports_dir, f"products_swu_{today_date}.csv")
}

# Filter and export products per game, removing specified columns
for game_id, file_name in game_files_mapping.items():
    # Filter products for the specific game
    df_game = df_products[df_products['game_id'] == game_id]
    
    # Remove specified columns
    df_game = df_game.drop(columns=columns_to_remove, errors='ignore')
    
    # Identify and remove columns starting with specific prefixes
    prefixes = prefixes_to_check.get(game_id, [])
    columns_to_drop = [col for col in df_game.columns if any(col.startswith(prefix) for prefix in prefixes)]
    df_game = df_game.drop(columns=columns_to_drop, errors='ignore')
    
    # Export the filtered and modified DataFrame to CSV
    df_game.to_csv(file_name, index=False)
    print(f"Products for game_id {game_id} exported successfully to {file_name}")

print(f"Products exported successfully to {products_file_name}")
print(f"Expansions exported successfully to {expansions_file_name}")
