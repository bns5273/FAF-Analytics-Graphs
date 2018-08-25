'''

'''


import plotly
import json
import numpy as np


with open('data/ladderleaderboard.json', 'r') as l:
    ladderl = json.loads(l.read())
with open('data/globalleaderboard.json', 'r') as g:
    globall = json.loads(g.read())

print(len(ladderl), 'total')

la, ga = [], []
for l, g in zip(ladderl, globall):
    lmean = l['attributes']['mean']
    ldev = l['attributes']['deviation']
    gmean = g['attributes']['mean']
    gdev = g['attributes']['deviation']

    if ldev < 80 and gdev < 100:
        la.append(lmean - 3 * ldev)
        ga.append(gmean - 3 * gdev)

print(len(la), 'valid')
print(np.corrcoef(la, ga)[0][1], 'correlation')

laddervglobal = [plotly.graph_objs.Scatter(
    x=la,
    y=ga,
    mode='markers'
)]

plotly.plotly.plot(laddervglobal, filename='laddervsglobal')
