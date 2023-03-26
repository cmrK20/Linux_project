#!/bin/bash

url="https://www.coindesk.com/price/ethereum/"
html="$(curl -s $url)"
price=$(echo "$html" | grep -oP '(?<=<span class="currency-pricestyles__Price-sc-1rux8hj-0 jIzQOt">)[^<]*')

echo $(date +%Y-%m-%d,%H:%M:%S),$price >> eth_price_history.csv
