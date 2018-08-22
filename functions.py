from math import sqrt
from trueskill import BETA
from trueskill.backends import cdf

def trueskill_1v1(a, b):
    delta_mu = a['beforeMean'] - b['beforeMean']
    denom = sqrt(2 * (BETA * BETA) + pow(a['beforeDeviation'], 2) + pow(b['beforeDeviation'], 2))
    return cdf(delta_mu / denom)


def trueskill_team(t1, t2):
    delta_mean = t1[0]['beforeMean'] + t1[1]['beforeMean'] + t1[2]['beforeMean'] + t1[3]['beforeMean'] - \
                 t2[0]['beforeMean'] - t2[1]['beforeMean'] - t2[2]['beforeMean'] - t2[3]['beforeMean']
    dev_a = t1[0]['beforeDeviation'] + t1[1]['beforeDeviation'] + t1[2]['beforeDeviation'] + t1[3]['beforeDeviation']
    dev_b = t2[0]['beforeDeviation'] + t2[1]['beforeDeviation'] + t2[2]['beforeDeviation'] + t2[3]['beforeDeviation']
    denom = sqrt(2 * (BETA * BETA) + pow(dev_a, 2) + pow(dev_b, 2))
    return cdf(delta_mean / denom)


def pRating(p):
    return p['beforeMean'] - 3 * p['beforeDeviation']


def isWinner(team):
    return max(team[0]['score'], team[1]['score'], team[2]['score'], team[3]['score']) > 0