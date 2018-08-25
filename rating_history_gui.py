# This is a simple GUI for displaying the rating history for a specific player and game mod.


import matplotlib
import tkinter as tk
import datetime
import json
import urllib.request

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class GraphPage(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.pack()

    def add_mpl_figure(self, fig):
        self.mpl_canvas = FigureCanvasTkAgg(fig, self)
        self.mpl_canvas.draw()
        self.mpl_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.mpl_canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class MPLGraph(Figure):

    def __init__(self, player, mod):
        Figure.__init__(self, figsize=(5, 5), dpi=150)
        self.plot = self.add_subplot(111)

        with urllib.request.urlopen("https://api.faforever.com/data/gamePlayerStats?"
                                    "filter=player.login=={0};"
                                    "game.featuredMod.technicalName=={1}"
                                    "&fields[gamePlayerStats]=afterMean,afterDeviation,faction,scoreTime"
                                    "&page[limit]=10000".format(player, mod)) as url:
            data = json.loads(url.read())
        # with open('data/spocko.json', 'r') as infile:
        #     data = json.loads(infile.read())

        colors = ['#00486b', '#005119', '#801609', '#9a751d']
        time = []
        rating = []
        faction = []

        for i in data['data']:
            f = int((i['attributes']['faction']) - 1)
            if i['attributes']['scoreTime'] is not None and i['attributes']['afterMean'] is not None and f < 4:
                time.append(datetime.datetime.strptime(i['attributes']['scoreTime'], '%Y-%m-%dT%H:%M:%SZ')
                            - datetime.timedelta(hours=8))
                rating.append(i['attributes']['afterMean'] - 3 * i['attributes']['afterDeviation'])
                faction.append(colors[f])

        self.plot.plot(time, rating, alpha=.5, c='black', linewidth=.8)
        self.plot.scatter(time, rating, color=faction, s=5)


root = tk.Tk()
root.title('FAF Rating History Tool')
root.geometry('800x600')
username = tk.Entry(root, width=20)
username.insert(0, 'Spocko')
username.pack()
mod = tk.Entry(root, width=20)
mod.insert(0, 'ladder1v1')
mod.pack()


def clicked():
    fig = MPLGraph(username.get(), mod.get())
    graph_page = GraphPage(root)
    graph_page.add_mpl_figure(fig)


btn = tk.Button(root, text='OK', command=clicked)
btn.pack()
root.mainloop()
