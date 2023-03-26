#!/bin/bash

url="https://www.marketwatch.com/investing/stock/aapl"
output_file="aapl_stock_price.txt"
dashboard_file="dashboard.html"
daily_report_file="daily_report.txt"
graph_file="graph.png"
data_file="data.csv"

# Fetch website content
content=$(curl -s $url)

# Extract data (example: AAPL stock price)
stock_price=$(echo "$content" | grep -oP '(?<=<bg-quote class="value" field="Last" format="0,0.00" channel="/zigman2/quotes/202934861/composite,/zigman2/quotes/202934861/lastsale" session="after">)[0-9,.]+')

# Write data to the output file with a timestamp only if the stock price is not empty
if [ -n "$stock_price" ]; then
  echo "$(date +"%Y-%m-%d %H:%M:%S"),$stock_price" >> $output_file
else
  echo "Failed to extract stock price. Check the script and website HTML structure."
fi

# Create dashboard HTML file with the latest AAPL stock price and graph
echo "<html><head><title>AAPL Stock Price</title></head><body><h1>AAPL Stock Price</h1><p>Last updated: $(date +"%Y-%m-%d %H:%M:%S")</p><p>Current price: $stock_price</p><img src=\"graph.png\"></body></html>" > $dashboard_file

# Create daily report file with several coherent metrics
daily_volatility=$(echo "$content" | grep -oP '(?<=Volatility">)[0-9,.]+%')
daily_open=$(echo "$content" | grep -oP '(?<=<span class="label">Open</span><span class="primary">)[0-9,.]+')
daily_close=$(echo "$content" | grep -oP '(?<=<span class="label">Close</span><span class="primary">)[0-9,.]+')
daily_change=$(echo "$content" | grep -oP '(?<=<span class="change--point--q">)[0-9,.]+')

echo "AAPL Daily Report" > $daily_report_file
echo "Date: $(date +"%Y-%m-%d")" >> $daily_report_file
echo "Daily volatility: $daily_volatility" >> $daily_report_file
echo "Daily open price: $daily_open" >> $daily_report_file
echo "Daily close price: $daily_close" >> $daily_report_file
echo "Daily price change: $daily_change" >> $daily_report_file

# Create data file
echo "timestamp,price" > $data_file
cat $output_file >> $data_file

# Create graph
python3 -c "import pandas as pd; import matplotlib.pyplot as plt; data = pd.read_csv('$data_file', index_col='timestamp', parse_dates=True); plt.plot(data); plt.savefig('$graph_file')"

# Update the dashboard HTML file, daily report file, and graph every 5 minutes using cron
# Add the following line to the crontab file (run "crontab -e" to edit):
# */5 * * * * /path/to/aapl_stock_price.sh
# This will run the script every 5 minutes and update the dashboard, daily report, and
