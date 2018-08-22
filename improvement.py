# This script retrieves various information on my game history.

import datetime
import json
import urllib.request

# 113982 or 51142
# faf or ladder1v1
with urllib.request.urlopen("https://api.faforever.com/data/gamePlayerStats?"
                            "filter=player.id==51142;game.featuredMod.technicalName==ladder1v1"
                            "&page[limit]=10000") as url:
    data = json.loads(url.read())

factions = ['uef', 'aeo', 'cyb', 'fim']

for i in data['data']:
    if i['attributes']['scoreTime'] is not None and i['attributes']['afterMean'] is not None:
        date = datetime.datetime.strptime(i['attributes']['scoreTime'], '%Y-%m-%dT%H:%M:%SZ') \
               - datetime.timedelta(hours=8)
        faction = factions[int((i['attributes']['faction']) - 1)]
        score = i['attributes']['score']
        beforeMean = i['attributes']['beforeMean']
        beforeDeviation = i['attributes']['beforeDeviation']
        afterMean = i['attributes']['afterMean']
        afterDeviation = i['attributes']['afterDeviation']
        print(date.date(), faction, score, afterMean, afterMean - beforeMean)
