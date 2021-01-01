#Import libraries
import requests
from bs4 import BeautifulSoup
import pandas
from collections import OrderedDict

#Fetch data of Player's ID
player_urls = pandas.read_csv("player_urls.csv")
urls = player_urls["URL Links"]

#Empty player list
player_list = []

#Positions
position_list = ["Defender", "Forward", "Goalkeeper", "Midfielder"]

#Iterate to scrap data of players from premierleague.com

for page in urls:
    #Using OrderedDict instead of Dict
    d=OrderedDict()
    #Fetching URLs one by one
    print(page)
    #Data Processing
    page_stats = requests.get(str(page)+"/stats")
    page_overview = requests.get(str(page)+"/overview")

    #Fetch webpage
    soup_stats = BeautifulSoup(page_stats.content, "html.parser")
    soup_overview = BeautifulSoup(page_overview.content, "html.parser")
    
    try:
        #Scraping Data
        #Scraping Data - Overview
        d['Nationality'] = soup_overview.find("span", {"class": "playerCountry"}).text.replace("\n","").strip()
        d['Position'] = player_position = soup_overview.find_all(class_='info')[1].text.replace("\n","").strip()
        
            ## Check if position is in list
        if d['Position'] not in position_list:
            d['Position'] = soup_overview.find_all(class_='info')[0].text.replace("\n","").strip()
        elif d['Position'] not in position_list:
            player_postion = soup_overview.find_all(class_='info')[2].text.replace("\n","").strip()
        elif d['Position'] not in position_list:
            player_postion = soup_overview.find_all(class_='info')[3].text.replace("\n","").strip()
        elif d['Position'] not in position_list:
            d['Position'] = ''
            
        d['Date of Birth'] = soup_overview.find('ul', attrs= {"class":"pdcol2"}).find('div',attrs={"class":"info"}).text.replace("\n","").strip()
        d['Height'] = soup_overview.find('ul', attrs= {"class":"pdcol3"}).find('div',attrs={"class":"info"}).text.replace("\n","").strip()


        #Scraping Data - Statistics
            #ATTACK
        d['Name'] = soup_overview.find('div', attrs= {"class":"playerDetails"}).find('div',attrs={"class":"name t-colour"}).text.replace("\n","").strip()
        d['Apps'] = soup_stats.find("span", {"class": "allStatContainer statappearances"}).text.replace("\n","").strip()
        d['Goals'] = soup_stats.find("span", {"class": "allStatContainer statgoals"}).text.replace("\n","").strip()
        d['Goals per Game'] = soup_stats.find("span", {"class": "allStatContainer statgoals_per_game"}).text.replace("\n","").strip()
        d['Shots']= soup_stats.find("span", {"class": "allStatContainer stattotal_scoring_att"}).text.replace("\n","").strip()
        d['Shots on Target'] = soup_stats.find("span", {"class": "allStatContainer statontarget_scoring_att"}).text.replace("\n","").strip()
        d['Shot Acc.'] = soup_stats.find("span", {"class": "allStatContainer statshot_accuracy"}).text.replace("\n","").strip()

            #TEAM PLAY
        d['Assists'] = soup_stats.find("span", {"class": "allStatContainer statgoal_assist"}).text.replace("\n","").strip()
        d['Passes'] = soup_stats.find("span", {"class": "allStatContainer stattotal_pass"}).text.replace("\n","").strip()
        d['Passes per Game'] = soup_stats.find("span", {"class": "allStatContainer stattotal_pass_per_game"}).text.replace("\n","").strip()
        d['Chances Created'] = soup_stats.find("span", {"class": "allStatContainer statbig_chance_created"}).text.replace("\n","").strip()
        d['Crosses'] = soup_stats.find("span", {"class": "allStatContainer stattotal_cross"}).text.replace("\n","").strip()
        d['Cross Acc.'] = soup_stats.find("span", {"class": "allStatContainer statcross_accuracy"}).text.replace("\n","").strip()

            #DISCIPLINE
        d['Yellow Cards'] = soup_stats.find("span", {"class": "allStatContainer statyellow_card"}).text.replace("\n","").strip()
        d['Red Cards'] = soup_stats.find("span", {"class": "allStatContainer statred_card"}).text.replace("\n","").strip()
        d['Fouls'] = soup_stats.find("span", {"class": "allStatContainer statfouls"}).text.replace("\n","").strip()
        d['Offsides'] = soup_stats.find("span", {"class": "allStatContainer stattotal_offside"}).text.replace("\n","").strip()

            #DEFENCE

        d['Tackles'] = soup_stats.find("span", {"class": "allStatContainer stattotal_tackle"}).text.replace("\n","").strip()
        d['Successful Tackles']= soup_stats.find("span", {"class": "allStatContainer stattackle_success"}).text.replace("\n","").strip()
        d['Blocked Shots'] = soup_stats.find("span", {"class": "allStatContainer statblocked_scoring_att"}).text.replace("\n","").strip()
        d['Interceptions'] = soup_stats.find("span", {"class": "allStatContainer statinterception"}).text.replace("\n","").strip()
        d['Clearances'] = soup_stats.find("span", {"class": "allStatContainer stattotal_clearance"}).text.replace("\n","").strip()
        d['Duels Won'] = soup_stats.find("span", {"class": "allStatContainer statduel_won"}).text.replace("\n","").strip()
        d['Duels Lost'] = soup_stats.find("span", {"class": "allStatContainer statduel_lost"}).text.replace("\n","").strip()
        d['Aerials Won'] = soup_stats.find("span", {"class": "allStatContainer stataerial_won"}).text.replace("\n","").strip()
        d['Aerials Lost'] = soup_stats.find("span", {"class": "allStatContainer stataerial_lost"}).text.replace("\n","").strip()
        d['50/50 Tackle Wins'] = soup_stats.find("span", {"class": "allStatContainer statwon_contest"}).text.replace("\n","").strip()
    except AttributeError:
        pass
        
    #Append dictionary to list
    player_list.append(d)
#Create a pandas DataFrame to store data and save it to .csv
df = pandas.DataFrame(player_list)
df.to_csv('Players_info.csv', index = False)
print("Success \n")
