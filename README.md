# FAF-Analytics-Graphs
UI (TkInter) ● JSON ● Plotly ● MatPlotLib ● Urllib ● Numpy ● RSQL filters

* rating_history_gui.py is a graphical tool that allows users to see a graph of their Supreme Commander online rating history.  
* analytics_factions.py retrieves data on Williamson's Bridge matches: the faction, mean, and deviation of both players. It then makes a hypothesis as to which faction provides an advantage. These graphs are probably the most elegant that I have made in this repo, you can view them below.   
* rating_history_matplotlib.py and rating_history_plotly.py provide various graphs of data downloaded from the api.faforever.com database.  
* analytics_games.py is a short script for printing out the most recent games of mine and displaying rating deltas, dates/times, etc.    
* analytics_leaderboards.py is another small script that I used to create some other interesting graphs using the database. I compare the ratings of players over the experience they have with the game.
* analytics_leaderboards_2.py uses similar data to make a comparison between players' performance in different game modes.  

Here are some of the graphs that I created with this project:  

analytics_factions.py:  
[win percentages by faction and rating](https://plot.ly/~bsse/45)  
[games played by faction and rating](https://plot.ly/~bsse/50)  
[games played by faction and date](https://plot.ly/~bsse/54)

analytics_leaderboards.py:  
[global rating over games played](https://plot.ly/~bsse/25)  
[ladder rating over games played](https://plot.ly/~bsse/27)  

analytics_leaderboards_2.py:  
[global rating over ladder rating](https://plot.ly/~bsse/23)

rating_history_plotly:  
[my rating over time](https://plot.ly/~bsse/12)  
[my rating over games](https://plot.ly/~bsse/14)  
[my rating over wins](https://plot.ly/~bsse/33)  
[my rating over losses](https://plot.ly/~bsse/35)  
