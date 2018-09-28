'''
This script retrieves data on ladder (1v1) matches: the faction, mean, and deviation of both players.
It then makes a hypothesis as to which faction provides an advantage in this game mode.
Using Plotly, I created a stacked histogram which shows some interesting trends.

This is the RSQL filter that can be used at api.faforever.com
game.featuredMod.technicalName==ladder1v1;game.mapVersion.id==593;game.validity=="VALID";beforeDeviation<80
'''


import json
import datetime
import plotly.plotly as py
import plotly.graph_objs as go
import urllib.request


dl = False

with open('ladder.json', 'r') as file:
    ld = json.loads(file.read())
# ld = []
print(len(ld), 'entries')
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
        if len(new) < 10000:
            break
    with open('ladder.json', 'w') as outfile:
        json.dump(ld, outfile)


factionWins = [[], [], [], []]
factionRatings = [[], [], [], []]
factionDates = [[], [], [], []]


i = 0
while i < len(ld)-1:
    if int(ld[i]['id'])+1 != int(ld[i+1]['id']):
        i += 1
        continue
    if ld[i]['attributes']['scoreTime'] is None or ld[i+1]['attributes']['scoreTime'] is None:
        i += 2
        continue

    if ld[i]['attributes']['score'] == 1:
        winner = ld[i]
        loser = ld[i+1]
    else:
        winner = ld[i+1]
        loser = ld[i]

    am = winner['attributes']['beforeMean']
    ad = winner['attributes']['beforeDeviation']
    at = datetime.datetime.strptime(winner['attributes']['scoreTime'], '%Y-%m-%dT%H:%M:%SZ')
    bm = loser['attributes']['beforeMean']
    bd = loser['attributes']['beforeDeviation']
    bt = datetime.datetime.strptime(loser['attributes']['scoreTime'], '%Y-%m-%dT%H:%M:%SZ')

    j = winner['attributes']['faction'] - 1
    k = loser['attributes']['faction'] - 1

    factionWins[j].append(1)
    factionRatings[j].append(am - 3 * ad)
    factionDates[j].append(at)

    factionWins[k].append(0)
    factionRatings[k].append(bm - 3 * bd)
    factionDates[k].append(bt)

    i += 2


facNames = ['UEF', 'Aeon', 'Cybran', 'Seraphim']
colors = ['#00486b', '#005119', '#801609', '#9a751d']


winrate_rating_data = []
games_data = []
winrate_date_data = []
games_date_data = []
for i in range(4):
    winrate_rating_data.append(go.Histogram(
        x=factionRatings[i],
        y=factionWins[i],
        name=facNames[i],
        histfunc='avg',
        hoverinfo="x+y",
        marker=dict(
            color=colors[i]
        ),
        opacity=.65,
        autobinx=False,
        xbins=dict(
            start=100,
            end=2500,
            size=20
        )
    ))
    games_data.append(go.Histogram(
        x=factionRatings[i],
        name=facNames[i],
        marker=dict(
            color=colors[i]
        ),
        autobinx=False,
        xbins=dict(
            start=100,
            end=2500,
            size=20
        )
    ))
    winrate_date_data.append(go.Histogram(
        x=factionDates[i],
        y=factionWins[i],
        name=facNames[i],
        histfunc='avg',
        hoverinfo="x+y",
        marker=dict(
            color=colors[i]
        ),
        opacity=.65
    ))
    games_date_data.append(go.Histogram(
        x=factionDates[i],
        name=facNames[i],
        hoverinfo="x+y",
        marker=dict(
            color=colors[i]
        )
    ))
winrate_rating_fig = go.Figure(
    data=winrate_rating_data,
    layout=go.Layout(
        barmode='overlay',
        xaxis=dict(
            title='Player Rating'
        ),
        yaxis=dict(
            title='Win Rate'
        )
    )
)
games_fig = go.Figure(
    data=games_data,
    layout=go.Layout(
        barmode='stack',
        xaxis=dict(
            title='Player Rating'
        ),
        yaxis=dict(
            title='Games'
        )
    )
)
winrate_date_fig = go.Figure(
    data=winrate_date_data,
    layout=go.Layout(
        barmode='overlay',
        xaxis=dict(
            title='Date'
        ),
        yaxis=dict(
            title='Win Rate'
        )
    )
)
games_date_fig = go.Figure(
    data=games_date_data,
    layout=go.Layout(
        barmode='stack',
        xaxis=dict(
            title='Date'
        ),
        yaxis=dict(
            title='Games'
        )
    )
)
py.plot(winrate_rating_fig, filename='factions_winRate_rating')
# py.plot(games_fig, filename='factions_games_rating')
py.plot(winrate_date_fig, filename='factions_winRate_date')
# py.plot(games_date_fig, filename='factions_games_date')
