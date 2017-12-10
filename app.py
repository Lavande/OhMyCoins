#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import fetcher
from operator import itemgetter
from flask import Flask, render_template
app = Flask(__name__)


def pie(capital):
    sorted_cap = sorted(capital.items(), key=itemgetter(1), reverse=True)
    top = sorted_cap[:8]
    others = 0
    for i in sorted_cap[8:]:
        others += i[1]
    top.append(('Others', others))
    labels = [i[0] for i in top]
    values = [i[1] for i in top]
    length = len(labels)
    return (values, labels, length)

def bar(capital):
    sorted_cap = sorted(capital.items(), key=itemgetter(1), reverse=True)
    labels = [i[0] for i in sorted_cap]
    values = [i[1] for i in sorted_cap]
    length = len(labels)
    return (values, labels, length)

@app.route('/')
def chart():
    #TODO: This will take long. Need to display sth in the front-end while fetching data
    (total, capital, mycoins) = fetcher.fetch_data()
    
    coin_no_value = {}
    for i in mycoins.keys():
        if i not in capital.keys(): coin_no_value[i] = mycoins[i]
    
    table = []
    for i in mycoins.keys():
        row = []
        row.append(i)
        if i in capital.keys():
            row.append('{0:.4f}'.format(capital[i]/mycoins[i]))
            row.append(mycoins[i])
            row.append(capital[i])
            table.insert(0, row)
        else:
            row.append(0)
            row.append(mycoins[i])
            row.append(0)
            table.append(row)
    table = sorted(table, key=itemgetter(3), reverse=True)
        
    (pie_values, pie_labels, pie_length) = pie(capital)
    (bar_values, bar_labels, bar_length) = bar(capital)
    return render_template('index.html', table=table, total=total,
                           pie_values=pie_values, pie_labels=pie_labels, pie_length=pie_length,
                           bar_values=bar_values, bar_labels=bar_labels, bar_length=bar_length)    


if __name__ == '__main__':
    app.run(debug=True, port=5001)
    
   
