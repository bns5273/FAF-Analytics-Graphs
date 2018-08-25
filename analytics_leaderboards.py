import plotly
import datetime
import json
import numpy as np
import operator
import urllib.request

with open('/home/brett/PycharmProjects/data/1v1leaderboard.json', 'r') as l:
    ladderl = json.loads(l.read())['data']
with open('/home/brett/PycharmProjects/data/globalleaderboard.json', 'r') as g:
    globall = json.loads(g.read())['data']


ladderl = sorted(ladderl, key=lambda k: int(k['attributes']['id']))
globall = sorted(globall, key=lambda k: int(k['attributes']['id']))


lrate = []
grate = []
games = []
i = 0
j = 0
c = 1
while i < ladderl.__len__() -1 and j < globall.__len__() -1:
    l = ladderl[i]['attributes']
    g = globall[j]['attributes']
    lid = int(l['id'])
    gid = int(g['id'])
    if lid == gid:
        lrate.append(l['rating'])
        grate.append(g['rating'])
        games.append(int(l['num_games']) + int(g['num_games']))
        # print(c, '\t',
        #       l['mean'], l['deviation'], l['num_games'], '\t',
        #       g['mean'], g['deviation'], g['num_games'])
        j += 1
        i += 1
        c += 1
    elif lid > gid:
        j += 1
    elif gid > lid:
        i += 1

    if i >= ladderl.__len__():
        i -= 1
    if j >= globall.__len__():
        j -= 1
print(c)

laddervglobal = [plotly.graph_objs.Scatter(
    x=lrate,
    y=grate,
    mode='markers'
)]
laddervgames = [plotly.graph_objs.Scatter(
    x=games,
    y=lrate,
    mode='markers'
)]
globalvgames = [plotly.graph_objs.Scatter(
    x=games,
    y=grate,
    mode='markers'
)]

plotly.plotly.plot(laddervglobal, filename='laddervsglobal')
plotly.plotly.plot(laddervgames, filename='laddervgames')
plotly.plotly.plot(globalvgames, filename='globalvgames')

