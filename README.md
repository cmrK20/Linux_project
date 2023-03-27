# Linux_project

# Ethereum Price Dashboard

This is a Python project that scrapes the current price of Ethereum from the [CoinDesk](https://www.coindesk.com/price/ethereum/) website and displays it on a live dashboard using the [Dash](https://dash.plotly.com/) framework. The project also includes a daily report that calculates and displays several metrics for the Ethereum price time series.

## Prerequisites

To run this project, you will need:

- Python 3.6 or later
- The following Python packages: `pandas`, `dash`, `plotly`

You can install the required packages using pip:

pip install pandas dash plotly
## Getting started

To run the project, follow these steps:

1. Clone the Git repository to your local machine:

git clone https://github.com/cmrK20/ethereum-price-dashboard.git

2. Navigate to the project directory:

cd ethereum-price-dashboard

3. Run the `scrape_eth_price.sh` script to start scraping the Ethereum price:

./scrape_eth_price.sh

This script uses `curl` to scrape the current price of Ethereum from the CoinDesk website every 5 minutes and stores it in a CSV file named `eth_price_history.csv`.

4. Open a new terminal window and navigate to the project directory.

5. Run the `dashboard.py` script to start the dashboard:


This script starts a local server that listens for incoming HTTP requests on port 8050. You can access the dashboard by opening a web browser and navigating to `http://13.53.44.105:8050`.

**Note:** For the best visualization of the Ethereum price time series, please press the 'Autoscale' button located at the top right corner of the graph. This will adjust the y-axis scale dynamically based on the range of data currently visible on the graph.

## Daily report

The daily report provides several coherent metrics for the Ethereum price time series, including:

- Price: The closing price of Ethereum at 8pm each day.
- Change (%): The percentage change in price from the previous day's closing price.
- Volatility: The 2-day rolling standard deviation of the percentage change in price.

The daily report is displayed below the Ethereum price time series graph on the dashboard.

## Notes

- This project is intended for educational purposes only and should not be used for financial or investment advice.
- Be careful to prevent any cost from your cloud provider if you are running the project on a hosted virtual machine.
- Hope this will be helpfull

