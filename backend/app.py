#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import fetcher
#import segments
import json
#from bs4 import BeautifulSoup
import config as cfg
from operator import itemgetter
from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


def pie(capital):
    sorted_cap = sorted(capital.items(), key=itemgetter(1), reverse=True)
    top = sorted_cap[:8]
    others = 0
    for i in sorted_cap[8:]:
        others += i[1]
    if others != 0: top.append(('Others', others))
    piedata = []
    for i in top:
        piedata.append({"name": i[0], "value": i[1]})
    return (piedata)


@app.route('/', methods=['POST', 'GET'])
def chart():
    cfg.other_bl = json.loads(request.form['other_bl'])
    form_addr = request.form['addresses']
    if form_addr != '': cfg.addresses = form_addr.split(', ')
    print(cfg.other_bl)
    print(cfg.addresses)

    #TODO: This will take long. Need to display sth in the front-end while fetching data
    (total, price, mycoins, capital) = fetcher.fetch_data()
    
    
    table = []
    for i in mycoins.keys():
        row = {}
        row["Token"] = i
        if i in capital.keys():
            row["Price"] = '{0:.4f}'.format(capital[i]/mycoins[i])
            row["Amount"] = mycoins[i]
            row["Value"] = capital[i]
            table.insert(0, row)
        else:
            row["Price"] = 0
            row["Amount"] = mycoins[i]
            row["Value"] = 0
            table.append(row)
    table = sorted(table, key=itemgetter("Value"), reverse=True)
        
    piedata = pie(capital)

#TODO: Crawl news and generate word cloud
#    cloud = segments.parseData()
    clouddata = []
#    for i in cloud.keys():
#        clouddata.append({"text": i, "weight": cloud[i]})


    return jsonify({"Table": table, "Total": total, "Pie": piedata, "Cloud": clouddata})

if __name__ == '__main__':
    app.run(debug=True, port=5050, host='0.0.0.0')
    
   
