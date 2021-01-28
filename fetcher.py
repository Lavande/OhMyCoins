#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import requests
import hashlib
import hmac
import time
import json
import urllib.parse
from uuid import uuid1
from itertools import count
from datetime import datetime
from bs4 import BeautifulSoup
import config as cfg


def dict_add(a, b):
    for k2, v2 in b.items():    
        if k2 in a.keys():
            a[k2] += v2
        else:
            a[k2] = v2
    return a


def get_ether(address):
    #This URL just works to circumvent the anti-crawler mechanism but don't know why --!
    url = 'https://cn.etherscan.com/tokenholdingsHandler.ashx?&a={0}&q=&p=1&f=0&h=0&sort=total_price_usd&order=desc&pUsd24hrs=128.33&pBtc24hrs=0.03389&pUsd=126.74&fav='.format(address)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url, headers=headers)
    html = r.json()['layout']
    soup = BeautifulSoup(html, 'html.parser')
    balancelist = soup.find_all('tr')
    assets = {}
    for i in balancelist:
        token = i.find_all('td')[2].text
        amount = float(i.find_all('td')[3].text.replace(',', ''))
        if token in assets.keys():
            print('Warning: Duplicated token symbol {0}. Using the first one.'.format(token))
            continue
        assets[token] = amount

    return assets


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


def get_bitfinex(apikey, apisecret):
    baseurl = 'https://api.bitfinex.com/'
    path = 'v2/auth/r/wallets'
    nonce = str(datetime.timestamp(datetime.now()))
    body = {}
    rawBody = json.dumps(body)
    signature = "/api/" + path + nonce + rawBody
    signature = hmac.new(apisecret, signature.encode('utf-8'), hashlib.sha384).hexdigest()
    headers = {
                "bfx-nonce": nonce,
                "bfx-apikey": apikey,
                "bfx-signature": signature,
                "content-type": "application/json"
            }
    r = requests.post(baseurl+path, headers=headers, data=rawBody, verify=True)
    
    balance = r.json()
    assets = {}
    for i in balance:
        token = i[1]
        amount = i[2]
        if amount == 0: continue
        assets[token] = amount
    return assets


def get_price_cg(coins):
    capital = {}
    #TODO: support coingecko
    return capital


def get_price_cmc(coins):
    capital = {}
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
      'start':'1',
      'limit':'500',
      'convert':'CNY'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': cfg.cmc_apikey
    }

    r = requests.get(url, params=parameters, headers=headers)
    prices = r.json()['data']

    for i in prices:
        token = i['symbol']
        #TODO: workaround for different use of symbols across platforms, but there must be a neat way!
        if i['slug'] == 'iota': token = 'IOT'
        if i['slug'] == 'kingn-coin': token = 'KNGC'
        if i['slug'] == 'cryptonex': token = 'CNXCOIN'
        if i['slug'] == 'latoken': token = 'LA'
        if i['slug'] == 'propy': token = 'PROP'
        if i['slug'] == 'selfkey': token = 'SKEY'
        if i['slug'] == 'presearch': token = 'PRSC'
        if i['slug'] == 'prochain': token = 'PRO'
        if i['slug'] == 'phoenixcoin': token = 'PHXC'
        if i['slug'] == 'key': token = 'BHKEY'
        if i['slug'] == 'airtoken': token = 'AIRT'
        if i['slug'] == 'eosdac': token = 'eosDAC'
        if token in coins.keys():
            capital[token] = float(i['quote']['CNY']['price']) * coins[token]

    return capital


def refresh_position():
    mycoins = cfg.other_bl
    
    #Etherscan
    if cfg.addresses != []:
        for address in cfg.addresses:
            assets = get_ether(address)
            print(address)
            print(str(assets))
            mycoins = dict_add(mycoins, assets)
        
    #Bittrex 
    if cfg.bittrex_apikey != '':
        assets = get_bittrex(cfg.bittrex_apikey, cfg.bittrex_apisecret)
        mycoins = dict_add(mycoins, assets)
    
    #Poloniex
    if cfg.poloniex_apikey != '':
        assets = get_poloniex(cfg.poloniex_apikey, cfg.poloniex_apisecret)
        mycoins = dict_add(mycoins, assets)
    
    #Bitfinex
    if cfg.bitfinex_apikey != '':
        assets = get_bitfinex(cfg.bitfinex_apikey, cfg.bitfinex_apisecret)
        mycoins = dict_add(mycoins, assets)


    tempdic = {}
    for i in mycoins.keys():
        if mycoins[i] != 0: tempdic[i] = mycoins[i]
    mycoins = tempdic
            
    #Store position in a text file
    with open(sys.path[0] + '/position.log', 'w') as f:
        f.write(str(mycoins))

    return None
    
def get_position():
    with open(sys.path[0] + '/position.log', 'r') as f:
        mycoins = json.loads(f.read().replace('\'', '\"'))

    #coinmarketcap
    capital = get_price_cmc(mycoins)
    total = 0
    for i in capital.keys():
        total += capital[i]
        capital[i] = int(capital[i])
    total = int(total)
    #print(capital)
    
    #Write log
    with open(sys.path[0] + '/ohmycoin.log', 'a') as f:
        f.write(str(datetime.today()) + '\tTOTAL: ' + str(total) + '\n')
        f.write('COINS: ' + str(mycoins) + '\n')
        f.write('CAPITAL: ' + str(capital) + '\n\n')
        
    return (total, capital, mycoins)

