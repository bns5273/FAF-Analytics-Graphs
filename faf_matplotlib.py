import matplotlib.pyplot as plt
import datetime
import json
import urllib.request
import numpy as np


player = 'Spocko'
mod = 'ladder1v1'
download = False

if download:
    with urllib.request.urlopen("https://api.faforever.com/data/gamePlayerStats?"
                                "filter=player.login=={0};"
                                "game.featuredMod.technicalName=={1}"
                                "&fields[gamePlayerStats]=afterMean,afterDeviation,faction,scoreTime"
                                "&page[limit]=10000".format(player, mod)) as url:
        data = json.loads(url.read())
        with open('data/spocko.json', 'w') as outfile:
            json.dump(data, outfile)
else:
    with open('data/spocko.json', 'r') as infile:
        data = json.loads(infile.read())
# print(data)


colors = ['#00486b', '#005119', '#801609', '#9a751d']
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

recent = 100    # most recent games only
template = '{0:9} {1:<6} {2:<8.{prec}} {3:<8.{prec}} {4:<6} {5:<6}'
print(template.format('faction', 'games', 'win %', 'a.r.d.', 'max',  'last', prec=8))
for f, wp, rd, r, in zip(factions, f_winperc, f_rDelta, f_rating):
    print(template.format(f, len(wp), np.mean(wp[-recent:]), np.mean(rd[-recent:]), int(np.max(r)), int(r[-1]), prec=4))


# plt.figure(dpi=300)
plt.plot(time, rating, alpha=.5, c='black', linewidth=.8)
plt.scatter(time, rating, color=faction, s=5)
plt.show()
# plt.savefig("g.png")
