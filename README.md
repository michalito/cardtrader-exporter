# CardTrader Exporter

This project is a Python application designed to export product and expansion data from CardTrader and format it for import into TCGPowerTools. The application leverages the CardTrader API to fetch data and outputs it into structured CSV files. While its primary use is for integration with TCGPowerTools, it can be used generically for any CardTrader export purposes.

## Features

- Fetches product and expansion data from CardTrader via their API.
- Transforms and exports product data into general and game-specific CSV files.
  - Includes transformation of price from cents to euros.
  - Expands nested JSON data into separate columns.
  - Renames columns as needed.
  - Filters and removes specific columns from game-specific exports.
  - Removes columns from game-specific exports based on specified prefixes.
- Automatically handles nested data structures and dynamically creates columns for nested values.

## Getting Started

### Prerequisites

- Docker installed on your system.
- A CardTrader API token, which can be obtained from your CardTrader profile settings.

### Setup

1. Clone the repository:

   ```sh
   git clone https://github.com/michalito/cardtrader-exporter.git
   cd cardtrader-exporter
   ```

2. Create a `.env` file to securely store your API token:

   ```sh
   echo "API_TOKEN=YOUR_AUTH_TOKEN" > .env
   ```

3. Build the Docker image:

   ```sh
   docker build -t cardtrader-exporter .
   ```

### Running the Application

1. Run the Docker container, providing the API token:

   ```sh
   docker run --env-file .env -v ${PWD}:/usr/src/app cardtrader-exporter
   ```

   This command mounts the current directory to the container's `/usr/src/app` directory and uses the `.env` file to set the `API_TOKEN` environment variable.

### Obtaining Your API Token

To authenticate and authorize API calls to CardTrader, you need an API token. You can obtain this token by:

1. Logging in to your CardTrader account.
2. Navigating to the settings page on your CardTrader profile.
3. Copying the token from the API section on the settings page.

Alternatively, you can copy the token directly from [CardTrader API Documentation](https://www.cardtrader.com/docs/api/full/reference) if you are logged in.

### Output Files

The application generates the following output files, saved in the `exports` directory:

1. `products_<date>.csv`: General product export.
2. `expansions_<date>.csv`: General expansions export.
3. `products_mtg_<date>.csv`: Magic: The Gathering specific product export.
4. `products_pokemon_<date>.csv`: Pokemon specific product export.
5. `products_fab_<date>.csv`: Flesh And Blood specific product export.
6. `products_lorcana_<date>.csv`: Lorcana specific product export.
7. `products_swu_<date>.csv`: Star Wars Unlimited specific product export.

### Note

If there are no products listed for a specific game, the application will skip generating the CSV file for that game.

### Features in Detail

- **Fetching and Exporting Data**: The application uses the CardTrader API to fetch product and expansion data and exports this data into CSV files, formatted for import into TCGPowerTools or other applications.
  
- **Dynamic Column Creation**: The `properties_hash` column, containing nested data, is expanded into separate columns dynamically, based on the nested key-value pairs found in each entry.

- **Column Renaming and Transformation**: Specific columns like `name_en` are renamed to `name`, and price values are transformed from cents to euros.

- **Column Filtering**: Game-specific exports have specific columns removed, ensuring only relevant data is included. Additionally, columns starting with specified prefixes (e.g., `mtg`, `fab`, etc.) are removed from the respective game-specific exports.

### Supported Games

Currently supported games include:

- Magic: The Gathering
- Pokemon
- Flesh And Blood
- Lorcana
- Star Wars Unlimited

### Security Note

It is recommended to store your `API_TOKEN` securely using environment variables, as demonstrated above, or using secrets management tools if deploying in a production environment. Avoid hardcoding sensitive tokens directly in the code.

## Contributing

If you would like to contribute to the project, please fork the repository and create a pull request. Contributions are always welcome.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.