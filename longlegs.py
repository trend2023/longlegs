#! /usr/bin/env python3
"""
Binance Smart Chain BEP20 Utility tool
Simple chain crawler of specific token's net gain/loss for specific wallet(s),
Depending on data provided in CSV file.

"""

from bs4 import BeautifulSoup
import requests
import csv
import time

# have to provide csv file with tx list from bscscan
data_file = "export-token-0x5e90253fbae4dab78aa351f4e6fed08a64ab5590.csv" # - bonfire token tx list, filtered by one dev's wallet

# token settings
token_contract = "0x5e90253fbae4dab78aa351f4e6fed08a64ab5590"  		# - bonfire token
pancake_address = "0xd3f478f0d5e98b01f757bc6cb54db4c00b9838f2" 		# - bonfire token pancake swap
pancake_str = "PancakeSwap: BONFIRE 2"                         		# - bonfire token key string for parcing (exact name of liquidity pool contract)


def get_swap(txID):  
  global pancake_str

  tx_url = 'https://bscscan.com/tx/'+txID
  page = requests.get(tx_url)
  soup = BeautifulSoup(page.text, 'html.parser')
  bnb_soup = soup.find_all("span", class_="mr-1")
  add_soup = soup.find_all("span", {"id":"spanFromAdd"})
  address = ""
  for y in add_soup:
    if len(y.get_text())> 40 :
      address = y.get_text()

  soup_list = []
  for x in bnb_soup:
    soup_list.append(x.get_text())
  token_index = 0
  bnb_index = 0
  counter = 0
  bnb = ""
  for i in soup_list:
    if pancake_str in i:
      token_index = counter
    if "$" in i:
      bnb_index = counter
      temp = i.split()
      bnb = temp[0]
    counter = counter + 1
  if (token_index > 0) and (bnb_index>0):
    if token_index < bnb_index:
      txtype = "sell"
    else:
      txtype = "buy"
  else:
    txtype = "none"
  tx_dict={}
  tx_dict["address"] = address
  tx_dict["type"] = txtype
  tx_dict["bnb"] = bnb
  return tx_dict


with open(data_file, newline='') as f:
  reader = csv.reader(f)
  data_list = list(reader)



buy_list = {}
sell_list = {}
for x in data_list:
  tx_data = get_swap(x[0]) 
  print(tx_data)
  addr = tx_data["address"]
  #if addr not in excluded:
  if tx_data["type"] == "buy":
    if addr in buy_list:
      buy_list[addr] = str(float(buy_list[addr]) + float(tx_data["bnb"]))
    else:
      buy_list[addr] = tx_data["bnb"]
  if tx_data["type"] == "sell":
    if addr in sell_list:
      sell_list[addr] = str(float(sell_list[addr]) + float(tx_data["bnb"]))
    else:
      sell_list[addr] = tx_data["bnb"]
  
  if addr in buy_list:
    buys = buy_list[addr]
  else:
    buys = "0.0"

  if addr in sell_list:
    sells = sell_list[addr]
  else:
    sells = "0.0"
 
  netg = str(float(sells) - float(buys))
  print("          Totals >>  buys: ", buys, "   sells: ", sells, "  gains: ", netg)
  time.sleep(1) 

print("Number of wallets: ", len(buy_list))
print("List:")
print("   Address                         ::  BNB spent (buys)        ::  BNB received (sells)     ::  BNB net gains/losses")
for addr in buy_list:
  netgains = str(float(sell_list[addr]) - float(buy_list[addr]))
  print(addr, "  ::  ", buy_list[addr], "   ::   ", sell_list[addr], "  ::  ", netgains)





