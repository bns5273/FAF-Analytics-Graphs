import plotly
import datetime
import json
import urllib.request
import numpy as np


download = False

if download:
    with urllib.request.urlopen("https://api.faforever.com/data/gamePlayerStats?"
                                "filter=player.login==Spocko;game.featuredMod.technicalName==ladder1v1"
                                "&fields[gamePlayerStats]=afterMean,afterDeviation,faction,scoreTime"
                                "&page[limit]=10000") as url:
        data = json.loads(url.read())
        with open('data/spocko.json', 'w') as outfile:
            json.dump(data, outfile)
else:
    with open('data/spocko.json', 'r') as infile:
        data = json.loads(infile.read())
# print(data)


colors = ['rgb(0, 72, 107)', 'rgb(0, 81, 25)', 'rgb(128, 22, 9)', 'rgb(154, 117, 29)']
factions = ['uef', 'aeon', 'cybran', 'seraphim']
time = []
losses = [0]
wins = [0]
rating = []
faction = []
f_winperc = [[], [], [], []]
f_rDelta = [[], [], [], []]
f_rating = [[], [], [], []]

for i in data['data']:
    f = int((i['attributes']['faction']) - 1)
    if i['attributes']['scoreTime'] is not None and i['attributes']['afterMean'] is not None and f < 4:
        time.append(datetime.datetime.strptime(i['attributes']['scoreTime'], '%Y-%m-%dT%H:%M:%SZ')
                    - datetime.timedelta(hours=8))
        rating.append(i['attributes']['afterMean'] - 3 * i['attributes']['afterDeviation'])
        faction.append(colors[f])
        if rating.__len__() > 1:
            result = rating[-1] > rating[-2]

            losses.append(losses[-1] + int(not result))  # accumulated number of losses
            wins.append(wins[-1] + int(result))  # accumulated number of wins
            f_winperc[f].append(result)
            f_rDelta[f].append(rating[-1] - rating[-2])
        f_rating[f].append(rating[-1])

recent = 150    # most recent games only
template = '{0:9} {1:<6} {2:<8.{prec}} {3:<8.{prec}} {4:<6} {5:<6}'
print(template.format('faction', 'games', 'win %', 'a.r.d.', 'max',  'last', prec=8))
for f, wp, rd, r, in zip(factions, f_winperc, f_rDelta, f_rating):
    print(template.format(f, len(wp), np.mean(wp[-recent:]), np.mean(rd[-recent:]), int(np.max(r)), int(r[-1]), prec=4))

overTime = [plotly.graph_objs.Scatter(
    x=time,
    y=rating,
    marker=dict(
        color=faction
    ),
    line=dict(
        color='rgb(150, 150, 150)'
    ),
    mode='lines+markers'
)]
overGames = [plotly.graph_objs.Scatter(
    x=list(range(time.__len__())),
    y=rating,
    marker=dict(
        color=faction
    ),
    line=dict(
        color='rgb(150, 150, 150)'
    ),
    mode='lines+markers'
)]
overLosses = [plotly.graph_objs.Scatter(
    x=losses,
    y=rating,
    marker=dict(
        color=faction
    ),
    line=dict(
        color='rgb(150, 150, 150)'
    ),
    mode='lines+markers'
)]
overWins = [plotly.graph_objs.Scatter(
    x=wins,
    y=rating,
    marker=dict(
        color=faction
    ),
    line=dict(
        color='rgb(150, 150, 150)'
    ),
    mode='lines+markers'
)]

# plotly.plotly.plot(overTime, filename='overTime')
# plotly.plotly.plot(overGames, filename='overGames')
# plotly.plotly.plot(overLosses, filename='overLosses')
# plotly.plotly.plot(overWins, filename='overWins')
