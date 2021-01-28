## CONFIG ##
## Leave it for blank if you don't want to include data from that source
## Rename this file to 'config.py' after editing.


#You NEED this key to use CMC APIs
#CoinMarketCap API Key
cmc_apikey = ''


#Ether addresses that you'd like to watch. Input them as a list if there're more than one address.
#E.g.: addresses = ['0xad2a6d5890c06083c340d723053b4040a28580ef', '0x214d0bb2b260b22b1498977200c1a32bdb75131b']
addresses = []


#Get this from Bittrex pannel. Watch-only permmision recommended
bittrex_apikey = ''
bittrex_apisecret = b''

#Get this from Poloniex pannel. Watch-only permmision recommended
poloniex_apikey = ''
poloniex_apisecret = b''

#Get this from Bitfinex pannel. Watch-only permmision recommended
bitfinex_apikey = ''
bitfinex_apisecret = b''


#Mannually add balance from other sources that this program has not covered yet
#E.g.: other_bl = {'BTC': 5.2, 'ETH': 10}
other_bl = {}
