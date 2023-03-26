#!/bin/bash

url="https://www.coindesk.com/price/ethereum/"
html="$(curl -s $url)"
price=$(echo "$html" | grep -oP '(?<=<span class="currency-pricestyles__Price-sc-1rux8hj-0 jIzQOt">)[^<]*' | tr -d ',')

timestamp=$(date +"%Y-%m-%d %H:%M:%S")
echo "$timestamp,$price" >> /home/ec2-user/Linux_project/eth_price_history.csv

# Add logging
echo "[$timestamp] Price fetched: $price" >> /home/ec2-user/Linux_project/scrape_eth_price.log

