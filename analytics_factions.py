'''
This script retrieves data on Williamson's Bridge matches: the faction, mean, and deviation of both
players. It then makes a hypothesis as to which faction provides an advantage on this map.

This is the JSON url:
https://api.faforever.com/data/gamePlayerStats?fields[gamePlayerStats]=beforeDeviation,beforeMean,faction,score,scoreTime&filter=game.featuredMod.technicalName%3D%3Dladder1v1%3Bgame.mapVersion.id%3D%3D593%3Bgame.validity%3D%3D%22VALID%22%3BbeforeDeviation%3C80&page[offset]=20000&page[limit]=10000

This is the RSQL filter that can be used at api.faforever.com
game.featuredMod.technicalName==ladder1v1;game.mapVersion.id==593;game.validity=="VALID";beforeDeviation<80
'''

import numpy
import json
from math import sqrt
from trueskill import BETA
from trueskill.backends import cdf


def win_probability(am, ad, bm, bd):
    delta_mu = am - bm
    denom = sqrt(2 * (BETA * BETA) + pow(ad, 2) + pow(bd, 2))
    return cdf(delta_mu / denom)


with open('/home/brett/PycharmProjects/data/williamsons_bridge.json', 'r') as file:
    wb = json.loads(file.read())


factionW = [numpy.array([]), numpy.array([]), numpy.array([]), numpy.array([])]
factionP = [numpy.array([]), numpy.array([]), numpy.array([]), numpy.array([])]
factionR = [numpy.array([]), numpy.array([]), numpy.array([]), numpy.array([])]

i = 0
c = 0
while i < wb.__len__()-2:
    if int(wb[i]['id'])+1 != int(wb[i+1]['id']):
        c += 1
        i += 1
        continue
    i += 2

    if wb[i]['attributes']['score'] == 1:
        winner = wb[i]
        loser = wb[i+1]
    else:
        winner = wb[i+1]
        loser = wb[i]

    am = winner['attributes']['beforeMean']
    ad = winner['attributes']['beforeDeviation']
    bm = loser['attributes']['beforeMean']
    bd = loser['attributes']['beforeDeviation']

    prob = win_probability(am, ad, bm, bd)
    # if prob < .05 or prob > .95:
    #     continue

    j = winner['attributes']['faction'] - 1
    k = loser['attributes']['faction'] - 1
    factionW[j] = numpy.append(factionW[j], 1)
    factionP[j] = numpy.append(factionP[j], prob)
    factionR[j] = numpy.append(factionR[j], am - 3 * ad)
    factionW[k] = numpy.append(factionW[k], 0)
    factionP[k] = numpy.append(factionP[k], 1 - prob)
    factionR[j] = numpy.append(factionR[j], bm - 3 * bd)


template = '{0:4} {1:<8.{prec}} {2:<12.{prec}} {3:<12.{prec}}'
facs = ['uef', 'aeo', 'cyb', 'fim']
print(template.format('fac', 'win%', 'win%/rating', 'correl', prec=12))
for fac, w, p in zip(facs, factionW, factionP):
    print(template.format(fac, w.mean(), w.mean() / p.mean(), numpy.corrcoef(w, p)[0][1], prec=4))
