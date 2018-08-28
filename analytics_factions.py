'''
This script retrieves data on ladder (1v1) matches: the faction, mean, and deviation of both players.
It then makes a hypothesis as to which faction provides an advantage in this game mode.
Using Plotly, I created a stacked histogram which shows some interesting trends.

This is the RSQL filter that can be used at api.faforever.com
game.featuredMod.technicalName==ladder1v1;game.mapVersion.id==593;game.validity=="VALID";beforeDeviation<80
'''

import numpy
import json
from math import sqrt
import plotly.plotly as py
import plotly.graph_objs as go
import urllib.request
from trueskill import BETA
from trueskill.backends import cdf


def win_probability(am, ad, bm, bd):
    delta_mu = am - bm
    denom = sqrt(2 * (BETA * BETA) + pow(ad, 2) + pow(bd, 2))
    return cdf(delta_mu / denom)


dl = False

with open('/home/brett/Documents/Code/data/ladder.json', 'r') as file:
    ld = json.loads(file.read())
# ld = []
if dl:
    for page in range(20, 30):
        with urllib.request.urlopen("https://api.faforever.com/data/gamePlayerStats?"
                                    "fields[gamePlayerStats]=beforeDeviation,beforeMean,faction,score,scoreTime"
                                    "&filter=game.featuredMod.technicalName==ladder1v1"
                                    # "&game.mapVersion.id==593"
                                    "&game.validity==VALID"
                                    "&page[limit]=10000"
                                    "&page[offset]={}".format(page * 10000)) as url:
            new = json.loads(url.read())['data']
        ld += new
        print(page)
        if len(new) < 10000:
            break
    with open('/home/brett/Documents/Code/data/ladder.json', 'w') as outfile:
        json.dump(ld, outfile)


factionWins = [numpy.array([]), numpy.array([]), numpy.array([]), numpy.array([])]
factionProbs = [numpy.array([]), numpy.array([]), numpy.array([]), numpy.array([])]
factionRatings = [numpy.array([]), numpy.array([]), numpy.array([]), numpy.array([])]


i = 0
while i < ld.__len__()-3:
    if int(ld[i]['id'])+1 != int(ld[i+1]['id']):
        i += 1
        continue
    i += 2

    if ld[i]['attributes']['score'] == 1:
        winner = ld[i]
        loser = ld[i+1]
    else:
        winner = ld[i+1]
        loser = ld[i]

    am = winner['attributes']['beforeMean']
    ad = winner['attributes']['beforeDeviation']
    bm = loser['attributes']['beforeMean']
    bd = loser['attributes']['beforeDeviation']

    prob = win_probability(am, ad, bm, bd)
    # if prob < .2 or prob > .8:
    #     continue

    j = winner['attributes']['faction'] - 1
    k = loser['attributes']['faction'] - 1
    factionWins[j] = numpy.append(factionWins[j], 1)
    factionProbs[j] = numpy.append(factionProbs[j], prob)
    factionRatings[j] = numpy.append(factionRatings[j], am - 3 * ad)

    factionWins[k] = numpy.append(factionWins[k], 0)
    factionProbs[k] = numpy.append(factionProbs[k], 1 - prob)
    factionRatings[k] = numpy.append(factionRatings[k], bm - 3 * bd)

facNames = ['UEF', 'Aeon', 'Cybran', 'Seraphim']
colors = ['#00486b', '#005119', '#801609', '#9a751d']

template = '{0:10} {1:<8.{prec}} {2:<12.{prec}} {3:<9.{prec}} {4:<9.{prec}} {5:6}'
print(template.format('fac', 'win%', 'win%/prob%', 'correl', 'avg rating', 'games', prec=12))
for fac, w, p, r in zip(facNames, factionWins, factionProbs, factionRatings):
    print(template.format(fac, w.mean(), w.mean() / p.mean(), numpy.corrcoef(w, p)[0][1], r.mean(), len(w), prec=5))


data = []
for i in range(4):
    data.append(go.Histogram(
        x=factionRatings[i],
        y=factionWins[i],
        name=facNames[i],
        histfunc='avg',
        hoverinfo="x+y",
        marker=dict(
            color=colors[i]
        ),
        xbins=dict(
            start=-350,
            end=2350,
            size=10
        )
    ))

fig = go.Figure(
    data=data,
    layout=go.Layout(
        barmode='stack',
        xaxis=dict(
            title='Player Rating'
        ),
        yaxis=dict(
            title='Win Rate'
        )
    )
)
py.plot(fig, filename='factions_WB_winRate')
