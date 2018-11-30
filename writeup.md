# Introduction

Armed with a growing set of data analysis tools, I thought I’d take a shot at creating a model to predict the winner of the NBA’s annual MVP award. With the stats repository Basketball-Reference.com as my playground and on the verge of jumping in, I heard a solemn voice call from the pages of one of the best statistical analysis texts that I’ve found, Getting Started with Data Science by Murtaza Haider. Exactly what he said, I’ll never reveal. But it did get me thinking about doing some literature review - that is, what other work might I find on this topic?

You can follow this link to find the point where my target pivoted a bit. Initially, I was inclined to use individual stats as predictors for MVP outcomes. An unoriginal approach, sure, but something that would get the ball rolling. Their analysis found that using a combination of traditional stats (‘points per game’ etc) and so-called advanced stats, one could predict with a high degree of accuracy the winner of the vote. They concluded that the shortcomings of their model could be explained by the narrative that accompanies every MVP race, variously hyping up and toppling contenders over the course of the season.

I thought this would be a more interesting angle to explore and so from here I changed direction to give more consideration to the narrative context of the race. My hypothesis: the narrative factor is largely a reflection of team success. Why is team success so important? The fans and media alike are attracted to winning teams, focusing a greater spotlight on the players of those teams. Secondly, and more importantly, the best players are able to drive their teams to success. What value can a player have if their production doesn’t translate into wins. The ‘V’ ought to stand for something.

My favorite part of this theory: it’s simple. And simple beats complicated, well maybe not everytime, but certainly often. As a regular season award, we can base our analysis on the Wins-Loss record of past MVP winners. And with that let’s dig into the numbers.

## Gathering Data

Basketball-Reference.com ('BBR') provides records of each annual MVP vote that include the following data of interest: player name and team, first-place votes, total points won, and share of total points. Total points are a weighted measure of votes cast per player, found by taking the sum of each vote received after it has been multiplied by a scaled number (first place votes are multiplied by twelve points while second-place and below by smaller factors). Share of total points is the proportion of total points earned to maximum achievable points during that year. Because first-place votes are the only one enumerated, share of total points is the only indicator that BBR provides for how voters cast their other votes.

'''
#For clarity's sake, I'll import dependant libraries as needed
import numpy as np
import pandas as pd
import sqlite3

#connect to db and create container for voting data
db = sqlite3.connect('mvp_db')
df = pd.read_sql_query('SELECT * FROM mvp_voting',db)
df.head()
'''
