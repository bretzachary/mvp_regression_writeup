import requests
import bs4
import sqlite3
import pandas as pd
import numpy as np

with sqlite3.connect("mvp_db2") as db:
    cursor = db.cursor()
    try:
        cursor.execute('''DROP TABLE mvp_voting''')
    except:
        cursor.execute('''
    CREATE TABLE mvp_voting (id INTEGER PRIMARY KEY,year INTEGER,
    vote_rank INTEGER, player_name TEXT, player_age INTEGER,
    player_team TEXT, first_place_votes INTEGER, total_points INTEGER,
    max_points INTEGER, wins_curr_year INTEGER, wins_one_prior INTEGER,
    wins_two_prior INTEGER, wins_three_prior INTEGER, wins_four_prior INTEGER,
    wins_five_prior INTEGER)
        ''')
db.commit()

mvp_list_url = 'https://www.basketball-reference.com/awards/awards_{0}.html#mvp'
mvp_years = range(1994, 2019)
mvp_votes=[]

def get_html(years):
    for year in years:
        url = mvp_list_url.format(year)
        vote_page = requests.get(url)
        vote_page = bs4.BeautifulSoup(vote_page.text)
        vote_page = vote_page.select('#mvp tbody tr')
        
        strip_html(vote_page, year) 

def strip_html(vote_page,year):
    for player in vote_page:
        player = player.getText(",").split(",")
        player = [str(year)] + player
        player = player[0:8]
    
        mvp_votes.append(player)

get_html(mvp_years)

team_abbreivation_changes = {'NOP':'NOH', 'CHH':'CHA','SEA':'OKC','TOT':'TOR'}


def get_wins(team):
    
    if team in team_abbreivation_changes:
        team = team_abbreivation_changes[team]

    url= 'https://www.basketball-reference.com/teams/{0}/'.format(team)
    req = requests.get(url)
    soup = bs4.BeautifulSoup(req.text)

    table = soup.select('table' '#{0} tr'.format(team))
    team_table = []
    for row in table[1:]:
        row = row.getText(",").split(",")
        team_table.append(row[:6])
    
    for year in team_table:
        year[0] = int(year[0][:4]) + 1
        if year[3] == '*':
            year[3] = year[4]
            year[4] = year[5]
        year[:] = year[:5]

    team_table = pd.DataFrame(team_table)

    team_table.drop([1,2],axis=1, inplace=True)
        
    team_table.columns = ['Year_Ending', 'Wins', 'Losses']
    team_table.index = team_table['Year_Ending'] 
    team_table.drop('Year_Ending', axis=1, inplace=True)

    if 2012 in team_table.index and 1999 in team_table.index:
        team_table.loc[2012, 'Wins'] = round(int(team_table.loc[2012]['Wins'])* 82/66)
        team_table.loc[2012, 'Losses'] = round(int(team_table.loc[2012]['Losses'])* 82/66)
        team_table.loc[1999, 'Wins'] = round(int(team_table.loc[1999]['Wins'])* 82/50)
        team_table.loc[1999, 'Losses'] = round(int(team_table.loc[1999]['Losses'])* 82/50)
    
    return team_table

for player in mvp_votes:
    team = player[4]
    team_table = get_wins(team)
    
    for x in range(6):
        try:
            player.append(team_table.loc[int(player[0]) - x]['Wins'])
        except:
            player.append(np.nan)

    cursor.execute('''INSERT INTO mvp_voting (year,
    vote_rank, player_name, player_age,
    player_team, first_place_votes, total_points,
    max_points, wins_curr_year, wins_one_prior,
    wins_two_prior, wins_three_prior, wins_four_prior,
    wins_five_prior) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (player))
  
    db.commit()

db.close()