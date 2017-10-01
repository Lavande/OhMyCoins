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
    (capital, mycoins) = fetcher.fetch_data(fetcher.mycoins)
    for i in capital.keys():
        capital[i] = int(capital[i])
    (pie_values, pie_labels, pie_length) = pie(capital)
    (bar_values, bar_labels, bar_length) = bar(capital)
    return render_template('index.html', capital=capital, mycoins=mycoins,
                           pie_values=pie_values, pie_labels=pie_labels, pie_length=pie_length,
                           bar_values=bar_values, bar_labels=bar_labels, bar_length=bar_length)    


if __name__ == '__main__':
    app.run(debug=True)
    
   
