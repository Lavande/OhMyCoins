#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


#Put your Ether addresses here in the list
addresses = []


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


def dict_add(a, b):
    for k2, v2 in b.items():    
        if k2 in a.keys():
            a[k2] += v2
        else:
            a[k2] = v2
    return a


mycoins = {}
for address in addresses:
    assets = get_ether(address)
    mycoins = dict_add(mycoins, assets)
