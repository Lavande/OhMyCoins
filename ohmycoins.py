#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import hashlib
import hmac
import time
import urllib.parse
from itertools import count
from datetime import datetime
from bs4 import BeautifulSoup


#INPUT Ether addresses here you want to watch
addresses = ['', '', '']
#INPUT api details of bittrex and poloniex
bittrex_apikey = ''
bittrex_apisecret = b''
poloniex_apikey = ''
poloniex_apisecret = b''


mycoins = {}

def dict_add(a, b):
    for k2, v2 in b.items():    
        if k2 in a.keys():
            a[k2] += v2
        else:
            a[k2] = v2
    return a


#Etherscan
def get_ether(address):
    url = 'https://etherscan.io/address/' + address
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    eth = soup.find_all('table')[0].find_all('td')[1].text.replace('\n','').split(' ')[0]
    eth = float(eth.replace(',', ''))
    assets = {'ETH': eth}
    balancelist = soup.find(id='balancelist')
    for i in balancelist.find_all('li')[:-1]:
        br = i.a.br.text.split('@')[0]
        token = br.split(' ')[1]
        amount = float(br.split(' ')[0].replace(',', ''))
        if token in assets.keys():
            print('Warning: Duplicated token symbol {0}. Using the first one.'.format(token))
            continue
        assets[token] = amount
    return assets

for address in addresses:
    assets = get_ether(address)
    mycoins = dict_add(mycoins, assets)
    

#Bittrex
def get_bittrex(apikey, apisecret):
    nonce = str(datetime.timestamp(datetime.now()))
    url = 'https://bittrex.com/api/v1.1/account/getbalances?apikey={0}&nonce={1}'.format(apikey,nonce)
    sign = hmac.new(apisecret, url.encode('utf-8'), hashlib.sha512).hexdigest()
    
    
    headers = {'apisign': sign}
    r = requests.get(url, headers=headers)
    balance = r.json()['result']
    assets = {}
    for i in balance:
        token = i['Currency']
        amount = i['Balance']
        if amount == 0: continue
        assets[token] = amount
    return assets

assets = get_bittrex(bittrex_apikey, bittrex_apisecret)
mycoins = dict_add(mycoins, assets)



#Poloniex
def get_poloniex(apikey, apisecret):
    nonce_counter = count(int(time.time() * 1000))    
    url = 'https://poloniex.com/tradingApi'
    payload = {'command': 'returnCompleteBalances',
                'account': 'all',
                'nonce': next(nonce_counter)}
    paybytes = urllib.parse.urlencode(payload).encode('utf8')
    sign = hmac.new(apisecret, paybytes, hashlib.sha512)
    headers = {'Key': apikey,
               'Sign': sign.hexdigest()}
    
    r = requests.post(url, data=payload, headers=headers)
    balance = r.json()
    
    assets = {}
    for k in balance.keys():
        onOrders = float(balance[k]['onOrders'])
        available = float(balance[k]['available'])
        if onOrders + available == 0: continue
        assets[k] = onOrders + available
    return assets

assets = get_poloniex(poloniex_apikey, poloniex_apisecret)
mycoins = dict_add(mycoins, assets)

print(mycoins)



#coinmarketcap
capital = {}

url = 'https://api.coinmarketcap.com/v1/ticker/?convert=CNY&limit=100'
r = requests.get(url)
prices = r.json()

for i in prices:
    token = i['symbol']
    if token in mycoins.keys():
        capital[token] = float(i['price_cny']) * mycoins[token]
        
sum = 0        
for k,v in capital.items():
    sum += v
print(capital)
print('Only calculating coins with market capital in top 100.\nSUM in CNY: '+str(sum))
