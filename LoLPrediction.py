from enum import unique
import json
from pandas import DataFrame
import pandas as pd
from flask import jsonify
import time
import re
import numpy as np
from catboost import CatBoostClassifier
with open('new1.json') as f:
    jsondata = json.load(f)

import requests

#url = "https://feed.lolesports.com/livestats/v1/window/105658534675942306"


#querystring = {"startingTime":"2021-07-03T02:34:20.000Z"}

payload = ""
headers = {
    "authority": "feed.lolesports.com",
    "sec-ch-ua": "^\^"
}

date_dictionary = {'September': '09','October':'10','November': '11','December':'12','January': '01','February':'02','March': '03','April':'04',
'May': '05','June':'06','July': '07','August':'08'}

#print(jsondata)
#matches_id = jsondata['data'][0]['games']['id']
#time_id =  jsondata['data'][0]['startTime']
#roleBlue = jsondata['gameMetadata']['blueTeamMetadata']['participantMetadata'][0]['role']
#print(matches_id)
#print(time_id)
#matches_id = []
#time_id = []
#for i in jsondata['data']:
    #matches_id.append(i['games']['id'])
    #time_id.append(i['startTime'])

with open('new1.json') as f:
    jsondata = json.load(f)

matches_id = []
time_id = []
for i in jsondata['events']:
    matches_id.append(i['games'][0]['id'])
    time_id.append(i['startTime'])
#print(matches_id[0])
#print(time_id[0])

matches_id = []
time_id = []
GameId = pd.read_csv('GameDataID.csv') 

matches_id.append(str(int(GameId.iloc[76,1]) + 1))

data = str(GameId.iloc[76,4])

data = data.split()
#print(data[0])
#print(data[1])
time_id.append("2021-"+str(date_dictionary[str(data[1])])+"-"+str(data[0])+"T"+str((int(GameId.iloc[76,2])-1))+":00:10.824Z")





def scraper(url,querystring,Time_Score_of_blue,Time_Score_of_red,time_step):
    url = "https://feed.lolesports.com/livestats/v1/window/"+str(url)
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    #print(response.text)
    jsondata = response.json()
    with open('personal.json', 'w') as json_file:
        json.dump(jsondata, json_file)

    with open('personal.json') as f:
        jsondata = json.load(f)
    particpants_of_blue_match = []
    particpants_of_red_match = []
    for participants in jsondata['gameMetadata']['blueTeamMetadata']['participantMetadata']:
        BluesummonerName = participants['summonerName']
        BluechampionId = participants['championId']
        Bluerole = participants['role']
        BlueparticipantId = participants['participantId']
        particpants_of_blue_match.append(['Blue',BluesummonerName,BluechampionId,Bluerole,BlueparticipantId])
    #particpants_of_blue_match = DataFrame(particpants_of_blue_match,columns=['Team','summonerName','championId','role','participantId'])


    for participants in jsondata['gameMetadata']['redTeamMetadata']['participantMetadata']:
        RedsummonerName = participants['summonerName']
        RedchampionIdBlue = participants['championId']
        RedroleBlue = participants['role']
        RedparticipantId = participants['participantId']
        particpants_of_red_match.append(['Red',RedsummonerName,RedchampionIdBlue,RedroleBlue,RedparticipantId])
    #particpants_of_red_match = DataFrame(particpants_of_red_match,columns=['Team','summonerName','championId','role','participantId'])


    #participants = pd.concat([particpants_of_blue_match, particpants_of_red_match], axis=1)

    #print(participants)


    for time_steps in jsondata['frames']:
        time = time_steps['rfc460Timestamp']
        BlueGold = time_steps['blueTeam']['totalGold']
        BlueInhibitors = time_steps['blueTeam']['inhibitors']
        BlueTowers = time_steps['blueTeam']['towers']
        BlueBarons = time_steps['blueTeam']['barons']
        BlueTotalKills = time_steps['blueTeam']['totalKills']
        RedGold = time_steps['redTeam']['totalGold']
        RedInhibitors = time_steps['redTeam']['inhibitors']
        RedTowers = time_steps['redTeam']['towers']
        RedBarons = time_steps['redTeam']['barons']
        RedTotalKills = time_steps['redTeam']['totalKills']
        i = 0
        for participants in time_steps['blueTeam']['participants']:
                BlueparticipantIdTime = participants['participantId']
                BluetotalGoldTime = participants["totalGold"]
                Bluelevel = participants["level"]
                Bluekills = participants["kills"]
                Bluedeaths = participants["deaths"]
                Blueassists = participants["assists"]
                BluecreepScore = participants["creepScore"]
                BluecurrentHealth = participants["currentHealth"]
                BluemaxHealth = participants["maxHealth"]

                Time_Score_of_blue.append([time_step,'Blue',time,BlueGold,BlueInhibitors,BlueTowers,BlueBarons,BlueTotalKills,BlueparticipantIdTime,BluetotalGoldTime,Bluelevel,
                Bluekills,Bluedeaths,Blueassists,BluecreepScore,BluecurrentHealth,BluemaxHealth,particpants_of_blue_match[i][1],particpants_of_blue_match[i][2],particpants_of_blue_match[i][3]])
                i = i + 1
        i = 0
        for participants in time_steps['redTeam']['participants']:
                RedparticipantIdTime = participants['participantId']
                RedtotalGoldTime = participants["totalGold"]
                Redlevel = participants["level"]
                Redkills = participants["kills"]
                Reddeaths = participants["deaths"]
                Redassists = participants["assists"]
                RedcreepScore = participants["creepScore"]
                RedcurrentHealth = participants["currentHealth"]
                RedmaxHealth = participants["maxHealth"]
                Time_Score_of_red.append(['Red',time,RedGold,RedInhibitors,RedTowers,RedBarons,RedTotalKills,RedparticipantIdTime,RedtotalGoldTime,Redlevel,
                Redkills,Reddeaths,Redassists,RedcreepScore,RedcurrentHealth,RedmaxHealth,particpants_of_red_match[i][1],particpants_of_red_match[i][2],particpants_of_red_match[i][3]])

                i = i + 1

    Time_Score_of_blue_dat = DataFrame(Time_Score_of_blue,columns=['Time','Team','time','BlueGold','BlueInhibitors','BlueTowers','BlueBarons','BlueTotalKills','BlueparticipantIdTime','BluetotalGoldTime','Bluelevel',
                'Bluekills','Bluedeaths','Blueassists','BluecreepScore','BluecurrentHealth','BluemaxHealth','BluesummonerName','BluesummonerID','Bluerole'])

    Time_Score_of_red_dat = DataFrame(Time_Score_of_red,columns=['Team','time','RedGold','RedInhibitors','RedTowers','RedBarons','RedTotalKills','RedparticipantIdTime','RedtotalGoldTime','Redlevel',
                'Redkills','Reddeaths','Redassists','RedcreepScore','RedcurrentHealth','RedmaxHealth','RedsummonerName','RedsummonerID','RedroleBlue'])      

    Time_Score = pd.concat([Time_Score_of_blue_dat, Time_Score_of_red_dat], axis=1)

    #particpants_of_blue_match.to_csv('particpants_of_blue_match.csv')
    #particpants_of_red_match.to_csv('particpants_of_red_match.csv')
    Time_Score_of_blue_dat.to_csv('Time_Score_of_blue.csv')
    Time_Score_of_red_dat.to_csv('Time_Score_of_red.csv')

    print(Time_Score)

    return Time_Score_of_blue, Time_Score_of_red
    
def scrapingtime(url,tijd,Time_Score_of_blue,Time_Score_of_red,time_step): 
    Time_Score_of_blue, Time_Score_of_red = scraper(url,tijd,Time_Score_of_blue,Time_Score_of_red,time_step)
    print("Waiting")
    time.sleep(25)
    return Time_Score_of_blue, Time_Score_of_red

def scrapingtime_live(url,tijd,Time_Score_of_blue,Time_Score_of_red,time_step): 
    Time_Score_of_blue, Time_Score_of_red = scraper(url,tijd,Time_Score_of_blue,Time_Score_of_red,time_step)
    print("Waiting")
    time.sleep(5)
    return Time_Score_of_blue, Time_Score_of_red

def finding_time(time,interval):
    time = str(time)
    m = re.search(':(.+?)Z', time)
    #print(time)
    mm = re.search(": '(.+?)T", time)
    if mm:
        date = mm.group(1)
        year = re.search('^(.+?)-', date)
        year = year.group(1)
        month = re.search('-(.+?)-', date)
        month = month.group(1)
        extract_day = re.search('-(.+?)$', date)
        day = re.search('-(.+?)$', extract_day.group(1))
        day = day.group(1)
        #print(date)
        if m:
            time = m.group(1)
            #print(time)
            m = re.search('T(.+?):', time)
            if m:
                hour = m.group(1)
                m = re.search('T'+str(hour)+':(.+?):', time)
                if m: 
                    minute = m.group(1)
                    minute = int(minute)
                    minute = minute + interval
                    if minute >= 60:
                        hour = int(hour) + 1 
                        minute = 0
                    if int(hour) >= 24:
                        hour = 0
                        day = int(day)+1
                        date = str(year)+'-'+str(month)+'-'+str(day)
                    tijd  = {"startingTime":str(date)+"T"+str(hour)+":"+str(minute)+":20.000Z"}
                    if len(str(minute)) == 1 : 
                        minute = "0"+str(minute)
                        tijd  = {"startingTime":str(date)+"T"+str(hour)+":"+str(minute)+":20.000Z"}
                    if len(str(hour)) == 1 : 
                        hour = "0"+str(hour)
                        tijd  = {"startingTime":str(date)+"T"+str(hour)+":"+str(minute)+":20.000Z"}
                    return tijd

def multiple_matches(url,tijd):
    tijd_id = []
    working = False
    idle = 0
    while working == False and idle < 61:
        tijd = finding_time(tijd,2)
        try:
            Time_Score_of_blue, Time_Score_of_red = scrapingtime(url,tijd,[],[],0)
            startpoint = tijd
            print(startpoint)
            working = True
        except: 
            print("Starting point not found")
            idle = idle + 1
    if idle < 61:
        for i in range(1,10):
            try:
                tijd  = finding_time(tijd,2)
                Time_Score_of_blue, Time_Score_of_red = scrapingtime(url,tijd,Time_Score_of_blue,Time_Score_of_red,i)
                tijd_id.append(i)
            except:
                print("Will not work")
        tijd_id = DataFrame(tijd_id,columns=['Time'])
        Time_Score_of_blue_dat = DataFrame(Time_Score_of_blue,columns=['Time','Team','time','BlueGold','BlueInhibitors','BlueTowers','BlueBarons','BlueTotalKills','BlueparticipantIdTime','BluetotalGoldTime','Bluelevel',
                    'Bluekills','Bluedeaths','Blueassists','BluecreepScore','BluecurrentHealth','BluemaxHealth','BluesummonerName','BluesummonerID','Bluerole'])

        Time_Score_of_red_dat = DataFrame(Time_Score_of_red,columns=['Team','time','RedGold','RedInhibitors','RedTowers','RedBarons','RedTotalKills','RedparticipantIdTime','RedtotalGoldTime','Redlevel',
                    'Redkills','Reddeaths','Redassists','RedcreepScore','RedcurrentHealth','RedmaxHealth','RedsummonerName','RedsummonerID','RedroleBlue'])      

        Time_Score = pd.concat([Time_Score_of_blue_dat, Time_Score_of_red_dat], axis=1)

        Time_Score = pd.concat([Time_Score, tijd_id], axis=1)

        return Time_Score

def changing_start_hour(time):
    time = str(time)
    m = re.search(':(.+?)Z', time)
    #print(time)
    mm = re.search(": '(.+?)T", time)
    if mm:
        date = mm.group(1)
        #print(str(date))
        if m:
            time = m.group(1)
            #print(time)
            m = re.search('T(.+?):', time)
            if m:
                hour = m.group(1)
                m = re.search('T'+str(hour)+':(.+?):', time)
                if m: 
                    minute = m.group(1)
                    minute = int(minute)
                    hour = int(hour)
                    hour = hour - 1
                    tijd  = {"startingTime":str(date)+"T"+str(hour)+":"+str(minute)+":20.000Z"}
                    if len(str(minute)) == 1 : 
                        minute = "0"+str(minute)
                        tijd  = {"startingTime":str(date)+"T"+str(hour)+":"+str(minute)+":20.000Z"}
                    if len(str(hour)) == 1 : 
                        hour = "0"+str(hour)
                        tijd  = {"startingTime":str(date)+"T"+str(hour)+":"+str(minute)+":20.000Z"}
                    return tijd   

def multiple_matches_live(url,tijd,timestep):
    tijd_id = []
    working = False
    idle = 0
    while working == False and idle < 61:
        tijd = finding_time(tijd,2)
        try:
            Time_Score_of_blue, Time_Score_of_red = scrapingtime_live(url,tijd,[],[],0)
            startpoint = tijd
            print(startpoint)
            working = True
        except: 
            print("Starting point not found")
            idle = idle + 1
    if working == False:
        print("Maximum Iteraties bereikt! ")
    if idle < 81:
        for i in range(1,timestep):
            try:
                tijd  = finding_time(tijd,2)
                print(tijd)
                Time_Score_of_blue, Time_Score_of_red = scrapingtime_live(url,tijd,Time_Score_of_blue,Time_Score_of_red,i)
                tijd_id.append(i)
            except:
                print("Will not work")
        tijd_id = DataFrame(tijd_id,columns=['Time'])
        Time_Score_of_blue_dat = DataFrame(Time_Score_of_blue,columns=['Time','Team','time','BlueGold','BlueInhibitors','BlueTowers','BlueBarons','BlueTotalKills','BlueparticipantIdTime','BluetotalGoldTime','Bluelevel',
                    'Bluekills','Bluedeaths','Blueassists','BluecreepScore','BluecurrentHealth','BluemaxHealth','BluesummonerName','BluesummonerID','Bluerole'])

        Time_Score_of_red_dat = DataFrame(Time_Score_of_red,columns=['Team','time','RedGold','RedInhibitors','RedTowers','RedBarons','RedTotalKills','RedparticipantIdTime','RedtotalGoldTime','Redlevel',
                    'Redkills','Reddeaths','Redassists','RedcreepScore','RedcurrentHealth','RedmaxHealth','RedsummonerName','RedsummonerID','RedroleBlue'])      

        Time_Score = pd.concat([Time_Score_of_blue_dat, Time_Score_of_red_dat], axis=1)

        Time_Score = pd.concat([Time_Score, tijd_id], axis=1)
        return Time_Score

def get_live_data(timestep,time_id,match_id):
    for i in range(0,1):
        print("Performing match "+ str(i))
        time = time_id
        time = {"startingTime":str(time)}
        time = changing_start_hour(time)
        if i == 0:
            print(match_id)
            Time_Score = multiple_matches_live(match_id,time,timestep)
        else:
            Time_score2 = multiple_matches_live(match_id,time,timestep)
            Time_Score = pd.concat([Time_Score, Time_score2],axis = 0)
    Time_Score.to_csv('Input_Data.csv')

def main():
    print(len(matches_id))
    for i in range(0,len(matches_id)):
        print("Performing match "+ str(i))
        time = time_id[i]
        time = {"startingTime":str(time)}
        #time = changing_start_hour(time)
        if i == 0:
            Time_Score = multiple_matches(matches_id[i],time)
        else:
            Time_score2 = multiple_matches(matches_id[i],time)
            Time_Score = pd.concat([Time_Score, Time_score2],axis = 0)

    Time_Score.to_csv('Time_Score_LCK2.csv')
    
#main()

#Below is for transforming the input data to a suitable format

def transforming_players(df):
    df = df.loc[:,['Time', 'Team', 'time', 'BlueGold', 'BlueInhibitors',
        'BlueTowers', 'BlueBarons', 'BlueTotalKills', 'BlueparticipantIdTime',
        'BluetotalGoldTime', 'Bluelevel', 'Bluekills', 'Bluedeaths',
        'Blueassists', 'BluecreepScore', 'BluecurrentHealth', 'BluemaxHealth',
        'BluesummonerName', 'BluesummonerID', 'Bluerole', 'Team.1', 'time.1',
        'RedGold', 'RedInhibitors', 'RedTowers', 'RedBarons', 'RedTotalKills',
        'RedparticipantIdTime', 'RedtotalGoldTime', 'Redlevel', 'Redkills',
        'Reddeaths', 'Redassists', 'RedcreepScore', 'RedcurrentHealth',
        'RedmaxHealth', 'RedsummonerName', 'RedsummonerID', 'RedroleBlue']]



    unique_time = np.unique(df[['time']])
    print(len(unique_time))
    unique_time_id = []
    for i in range(0,len(unique_time)):
        if (df['time'].values == unique_time[i] ).sum() == 5:
            unique_time_id.append(unique_time[i])
    print(len(unique_time_id))
    xx = []
    a = len(np.unique(df[['time']]))
    teller = 0
    for i in range(0,len(unique_time_id)):
        x = []
        data = df.loc[(df.time == (unique_time_id[i]))]
        data =  DataFrame(data,columns=['Time', 'Team', 'time', 'BlueGold', 'BlueInhibitors',
        'BlueTowers', 'BlueBarons', 'BlueTotalKills', 'BlueparticipantIdTime',
        'BluetotalGoldTime', 'Bluelevel', 'Bluekills', 'Bluedeaths',
        'Blueassists', 'BluecreepScore', 'BluecurrentHealth', 'BluemaxHealth',
        'BluesummonerName', 'BluesummonerID', 'Bluerole', 'Team.1', 'time.1',
        'RedGold', 'RedInhibitors', 'RedTowers', 'RedBarons', 'RedTotalKills',
        'RedparticipantIdTime', 'RedtotalGoldTime', 'Redlevel', 'Redkills',
        'Reddeaths', 'Redassists', 'RedcreepScore', 'RedcurrentHealth',
        'RedmaxHealth', 'RedsummonerName', 'RedsummonerID', 'RedroleBlue'])      
        
        x.append(data.iloc[0,0])
        x.append(data.iloc[0,2])
        x.append(data.iloc[0,3])
        x.append(data.iloc[0,4])
        x.append(data.iloc[0,5])
        x.append(data.iloc[0,6])
        x.append(data.iloc[0,7])

        x.append(data.iloc[0,22])
        x.append(data.iloc[0,23])
        x.append(data.iloc[0,24])
        x.append(data.iloc[0,25])
        x.append(data.iloc[0,26])

        for j in range(0,5):
            x.append(data.iloc[j,9])
            x.append(data.iloc[j,10])
            x.append(data.iloc[j,11])
            x.append(data.iloc[j,12])
            x.append(data.iloc[j,13])
            x.append(data.iloc[j,14])
            x.append(data.iloc[j,15])
            x.append(data.iloc[j,16])
            x.append(data.iloc[j,17])
            x.append(data.iloc[j,18])
            x.append(data.iloc[j,19])
            x.append(data.iloc[j,28])
            x.append(data.iloc[j,29])
            x.append(data.iloc[j,30])
            x.append(data.iloc[j,31])
            x.append(data.iloc[j,32])
            x.append(data.iloc[j,33])
            x.append(data.iloc[j,34])
            x.append(data.iloc[j,35])
            x.append(data.iloc[j,36])
            x.append(data.iloc[j,37])
            x.append(data.iloc[j,38])
        
        xx.append(x)
        teller += 5

    xx = DataFrame(xx,columns=['Time','time', 'BlueGold', 'BlueInhibitors', 'BlueTowers', 'BlueBarons', 'BlueTotalKills','RedGold', 'RedInhibitors', 'RedTowers', 'RedBarons', 'RedTotalKills',
                    'BluetotalGoldTime1','Bluelevel1','Bluekills1','Bluedeaths1','Blueassists1','BluecreepScore1','BluecurrentHealth1','BluemaxHealth1','BluesummonerName1','BluesummonerID1',
                    'Bluerole1','RedtotalGoldTime6','Redlevel6','Redkills6','Reddeaths6','Redassists6','RedcreepScore6','RedcurrentHealth6','RedmaxHealth6','RedsummonerName6','RedsummonerID6','RedroleBlue6',
                    
                    'BluetotalGoldTime2','Bluelevel2','Bluekills2','Bluedeaths2','Blueassists2','BluecreepScore2','BluecurrentHealth2','BluemaxHealth2','BluesummonerName2','BluesummonerID2',
                    'Bluerole2','RedtotalGoldTime7','Redlevel7','Redkills7','Reddeaths7','Redassists7','RedcreepScore7','RedcurrentHealth7','RedmaxHealth7','RedsummonerName7','RedsummonerID7','RedroleBlue7',
                    
                    'BluetotalGoldTime3','Bluelevel3','Bluekills3','Bluedeaths3','Blueassists3','BluecreepScore3','BluecurrentHealth3','BluemaxHealth3','BluesummonerName3','BluesummonerID3',
                    'Bluerole3','RedtotalGoldTime8','Redlevel8','Redkills8','Reddeaths8','Redassists8','RedcreepScore8','RedcurrentHealth8','RedmaxHealth8','RedsummonerName8','RedsummonerID8','RedroleBlue8',
                    
                    'BluetotalGoldTime4','Bluelevel4','Bluekills4','Bluedeaths4','Blueassists4','BluecreepScore4','BluecurrentHealth4','BluemaxHealth4','BluesummonerName4','BluesummonerID4',
                    'Bluerole4','RedtotalGoldTime9','Redlevel9','Redkills9','Reddeaths9','Redassists9','RedcreepScore9','RedcurrentHealth9','RedmaxHealth9','RedsummonerName9','RedsummonerID9','RedroleBlue9',
                    
                    'BluetotalGoldTime5','Bluelevel5','Bluekills5','Bluedeaths5','Blueassists5','BluecreepScore5','BluecurrentHealth5','BluemaxHealth5','BluesummonerName5','BluesummonerID5',
                    'Bluerole5','RedtotalGoldTime10','Redlevel10','Redkills10','Reddeaths10','Redassists10','RedcreepScore10','RedcurrentHealth10','RedmaxHealth10','RedsummonerName10','RedsummonerID10','RedroleBlue10'])      

    return xx

def transforming_time(df):
    #df = pd.read_csv('Time_Score_Changed.csv')
    print(df.columns)
    x = []
    i = 0
    j = 0 
    while i < df.shape[0] and j < df.shape[0]:
        j = i + 1 
        x.append(i)
        #print(i)
        if j < df.shape[0] and i < df.shape[0]:
            while df.iloc[i,0] == df.iloc[j,0] and j < df.shape[0] and i < df.shape[0]:
                j = j + 1
                if j >= df.shape[0]:
                    break
        i = j 

    Filter_df  = df[df.index.isin(x)]

    Filter_df = Filter_df.loc[:,['Time','time', 'BlueGold', 'BlueInhibitors', 'BlueTowers', 'BlueBarons', 'BlueTotalKills','RedGold', 'RedInhibitors', 'RedTowers', 'RedBarons', 'RedTotalKills',
                    'BluetotalGoldTime1','Bluelevel1','Bluekills1','Bluedeaths1','Blueassists1','BluecreepScore1','BluecurrentHealth1','BluemaxHealth1','BluesummonerName1','BluesummonerID1',
                    'Bluerole1','RedtotalGoldTime6','Redlevel6','Redkills6','Reddeaths6','Redassists6','RedcreepScore6','RedcurrentHealth6','RedmaxHealth6','RedsummonerName6','RedsummonerID6','RedroleBlue6',
                    
                    'BluetotalGoldTime2','Bluelevel2','Bluekills2','Bluedeaths2','Blueassists2','BluecreepScore2','BluecurrentHealth2','BluemaxHealth2','BluesummonerName2','BluesummonerID2',
                    'Bluerole2','RedtotalGoldTime7','Redlevel7','Redkills7','Reddeaths7','Redassists7','RedcreepScore7','RedcurrentHealth7','RedmaxHealth7','RedsummonerName7','RedsummonerID7','RedroleBlue7',
                    
                    'BluetotalGoldTime3','Bluelevel3','Bluekills3','Bluedeaths3','Blueassists3','BluecreepScore3','BluecurrentHealth3','BluemaxHealth3','BluesummonerName3','BluesummonerID3',
                    'Bluerole3','RedtotalGoldTime8','Redlevel8','Redkills8','Reddeaths8','Redassists8','RedcreepScore8','RedcurrentHealth8','RedmaxHealth8','RedsummonerName8','RedsummonerID8','RedroleBlue8',
                    
                    'BluetotalGoldTime4','Bluelevel4','Bluekills4','Bluedeaths4','Blueassists4','BluecreepScore4','BluecurrentHealth4','BluemaxHealth4','BluesummonerName4','BluesummonerID4',
                    'Bluerole4','RedtotalGoldTime9','Redlevel9','Redkills9','Reddeaths9','Redassists9','RedcreepScore9','RedcurrentHealth9','RedmaxHealth9','RedsummonerName9','RedsummonerID9','RedroleBlue9',
                    
                    'BluetotalGoldTime5','Bluelevel5','Bluekills5','Bluedeaths5','Blueassists5','BluecreepScore5','BluecurrentHealth5','BluemaxHealth5','BluesummonerName5','BluesummonerID5',
                    'Bluerole5','RedtotalGoldTime10','Redlevel10','Redkills10','Reddeaths10','Redassists10','RedcreepScore10','RedcurrentHealth10','RedmaxHealth10','RedsummonerName10','RedsummonerID10','RedroleBlue10']]
    Filter_df.to_csv('Filter_df2.csv')
    return Filter_df

def finding_minutes(time):
    time = {"startingTime":str(time)}
    time = str(time)
    m = re.search(':(.+?)Z', time)
    #print(time)
    mm = re.search(": '(.+?)T", time)
    if mm:
        date = mm.group(1)
        #print(str(date))
        if m:
            time = m.group(1)
            #print(time)
            m = re.search('T(.+?):', time)
            if m:
                hour = m.group(1)
                m = re.search('T'+str(hour)+':(.+?):', time)
                if m: 
                    minute = m.group(1)
                    minute = int(minute)
                    return minute

def checking_time(df):
    df = df.loc[:,['Time','time', 'BlueGold', 'BlueInhibitors', 'BlueTowers', 'BlueBarons', 'BlueTotalKills','RedGold', 'RedInhibitors', 'RedTowers', 'RedBarons', 'RedTotalKills',
                    'BluetotalGoldTime1','Bluelevel1','Bluekills1','Bluedeaths1','Blueassists1','BluecreepScore1','BluecurrentHealth1','BluemaxHealth1','BluesummonerName1','BluesummonerID1',
                    'Bluerole1','RedtotalGoldTime6','Redlevel6','Redkills6','Reddeaths6','Redassists6','RedcreepScore6','RedcurrentHealth6','RedmaxHealth6','RedsummonerName6','RedsummonerID6','RedroleBlue6',
                    
                    'BluetotalGoldTime2','Bluelevel2','Bluekills2','Bluedeaths2','Blueassists2','BluecreepScore2','BluecurrentHealth2','BluemaxHealth2','BluesummonerName2','BluesummonerID2',
                    'Bluerole2','RedtotalGoldTime7','Redlevel7','Redkills7','Reddeaths7','Redassists7','RedcreepScore7','RedcurrentHealth7','RedmaxHealth7','RedsummonerName7','RedsummonerID7','RedroleBlue7',
                    
                    'BluetotalGoldTime3','Bluelevel3','Bluekills3','Bluedeaths3','Blueassists3','BluecreepScore3','BluecurrentHealth3','BluemaxHealth3','BluesummonerName3','BluesummonerID3',
                    'Bluerole3','RedtotalGoldTime8','Redlevel8','Redkills8','Reddeaths8','Redassists8','RedcreepScore8','RedcurrentHealth8','RedmaxHealth8','RedsummonerName8','RedsummonerID8','RedroleBlue8',
                    
                    'BluetotalGoldTime4','Bluelevel4','Bluekills4','Bluedeaths4','Blueassists4','BluecreepScore4','BluecurrentHealth4','BluemaxHealth4','BluesummonerName4','BluesummonerID4',
                    'Bluerole4','RedtotalGoldTime9','Redlevel9','Redkills9','Reddeaths9','Redassists9','RedcreepScore9','RedcurrentHealth9','RedmaxHealth9','RedsummonerName9','RedsummonerID9','RedroleBlue9',
                    
                    'BluetotalGoldTime5','Bluelevel5','Bluekills5','Bluedeaths5','Blueassists5','BluecreepScore5','BluecurrentHealth5','BluemaxHealth5','BluesummonerName5','BluesummonerID5',
                    'Bluerole5','RedtotalGoldTime10','Redlevel10','Redkills10','Reddeaths10','Redassists10','RedcreepScore10','RedcurrentHealth10','RedmaxHealth10','RedsummonerName10','RedsummonerID10','RedroleBlue10']]
    for i in range(0,df.shape[0]):
        if df.iloc[i,0] == 0: 
            ref_minute = finding_minutes(df.iloc[i,1])
        else: 
            next_minute = finding_minutes(df.iloc[i,1])
            if next_minute < ref_minute:
                next_minute = next_minute + 60
            if next_minute - ref_minute != 2*df.iloc[i,0]:
                df.iloc[i,0] = round((next_minute - ref_minute)/2,0)
                
    return df

def setting_up_training_data(df,interval):
    df = df.loc[:,['BluesummonerName1','BluesummonerID1','Bluerole1','RedsummonerName6','RedsummonerID6','RedroleBlue6',
                    'BluesummonerName2','BluesummonerID2','Bluerole2','RedsummonerName7','RedsummonerID7','RedroleBlue7',
                    'BluesummonerName3','BluesummonerID3','Bluerole3','RedsummonerName8','RedsummonerID8','RedroleBlue8',
                    'BluesummonerName4','BluesummonerID4','Bluerole4','RedsummonerName9','RedsummonerID9','RedroleBlue9',
                    'BluesummonerName5','BluesummonerID5','Bluerole5','RedsummonerName10','RedsummonerID10','RedroleBlue10',

                    'Time', 'BlueGold', 'BlueInhibitors', 'BlueTowers', 'BlueBarons', 'BlueTotalKills','RedGold', 'RedInhibitors', 'RedTowers', 'RedBarons', 'RedTotalKills',
                    'BluetotalGoldTime1','Bluelevel1','Bluekills1','Bluedeaths1','Blueassists1','BluecreepScore1','BluecurrentHealth1','BluemaxHealth1',
                    'RedtotalGoldTime6','Redlevel6','Redkills6','Reddeaths6','Redassists6','RedcreepScore6','RedcurrentHealth6','RedmaxHealth6',
                    
                    'BluetotalGoldTime2','Bluelevel2','Bluekills2','Bluedeaths2','Blueassists2','BluecreepScore2','BluecurrentHealth2','BluemaxHealth2',
                    'RedtotalGoldTime7','Redlevel7','Redkills7','Reddeaths7','Redassists7','RedcreepScore7','RedcurrentHealth7','RedmaxHealth7',
                    
                    'BluetotalGoldTime3','Bluelevel3','Bluekills3','Bluedeaths3','Blueassists3','BluecreepScore3','BluecurrentHealth3','BluemaxHealth3',
                    'RedtotalGoldTime8','Redlevel8','Redkills8','Reddeaths8','Redassists8','RedcreepScore8','RedcurrentHealth8','RedmaxHealth8',
                    
                    'BluetotalGoldTime4','Bluelevel4','Bluekills4','Bluedeaths4','Blueassists4','BluecreepScore4','BluecurrentHealth4','BluemaxHealth4',
                    'RedtotalGoldTime9','Redlevel9','Redkills9','Reddeaths9','Redassists9','RedcreepScore9','RedcurrentHealth9','RedmaxHealth9',
                    
                    'BluetotalGoldTime5','Bluelevel5','Bluekills5','Bluedeaths5','Blueassists5','BluecreepScore5','BluecurrentHealth5','BluemaxHealth5'
                    ,'RedtotalGoldTime10','Redlevel10','Redkills10','Reddeaths10','Redassists10','RedcreepScore10','RedcurrentHealth10','RedmaxHealth10']]
    j = 0
    xx = []
    for i in range(0,df.shape[0]):
        x = []
        if 0 == df.iloc[i,30]:
            start = i
            compleet = True
            print(start)
            for a in range(0,30):
                x.append(df.iloc[start,a])
            for j in range(0,interval+1):
                if df.iloc[start+j,30] == j:
                    compleet = True
                    for a in range(30,len(df.columns)):
                        x.append(df.iloc[start+j,a])
                else: 
                    compleet = False
                    break
            if compleet == True:
                xx.append(x)
    column_names = ['BluesummonerName1','BluesummonerID1','Bluerole1','RedsummonerName6','RedsummonerID6','RedroleBlue6',
                    'BluesummonerName2','BluesummonerID2','Bluerole2','RedsummonerName7','RedsummonerID7','RedroleBlue7',
                    'BluesummonerName3','BluesummonerID3','Bluerole3','RedsummonerName8','RedsummonerID8','RedroleBlue8',
                    'BluesummonerName4','BluesummonerID4','Bluerole4','RedsummonerName9','RedsummonerID9','RedroleBlue9',
                    'BluesummonerName5','BluesummonerID5','Bluerole5','RedsummonerName10','RedsummonerID10','RedroleBlue10']
    for j in range(0,interval+1):
        for a in range(30,len(df.columns)):
            name = df.columns[a]
            column_names.append(name+str('Time')+str(j))
    xx = DataFrame(xx,columns=column_names)
    xx.to_csv('FINAL_DF.csv')

#df = pd.read_csv('Time_Score_LCS2.csv')     
#df = transforming_players(df)
#df = transforming_time(df)
#df = checking_time(df)
#setting_up_training_data(df,9)

# MAKING REAL TIME PREDICTIONS
# ITERATIVELY WITH THE MAIN2 COMMAND YOU CAN CHOOSE FOR A CERTAIN TIME

def main2(i):
    model = CatBoostClassifier()
    model.load_model("catboostmodel"+str(i))
    get_live_data(i+1)
    df = pd.read_csv('Input_Data.csv') 
    df = transforming_players(df)
    df = transforming_time(df)
    df = checking_time(df)
    setting_up_training_data(df,i)
    dfs = pd.read_csv('FINAL_DF.csv') 
    dfs = dfs.iloc[:,1:dfs.shape[1]]
    pred_labels = model.predict(dfs,prediction_type='Probability')
    print(pred_labels)
    pred_labels = model.predict(dfs)
    print(pred_labels)

#main2(9)

def setting_the_input(GameID,match,date,startuur):
    matches_id = []
    time_id = [] 
    matches_id.append(str(int(GameID) + int(match)))
    data = str(date)
    data = data.split()
    print(data[0])
    print(data[1])
    if (len(str(data[0])) == 1 ):
         data[0] = "0"+str(data[0])
    time_id.append("2021-"+str(date_dictionary[str(data[1])])+"-"+str(data[0])+"T"+str((int(startuur)-2+int(match)))+":00:10.824Z")
    print("You can find the result in following link: ")
    print("https://lolesports.com/vod/"+str(GameID)+"/"+str(match))
    return time_id[0],matches_id[0]


def FINALMODEL_PREDICTION(time_id,match_id):
    model1 = CatBoostClassifier()
    model1.load_model("catboostmodel2")

    model2 = CatBoostClassifier()
    model2.load_model("catboostmodel4")

    model3 = CatBoostClassifier()
    model3.load_model("catboostmodel6")

    model4 = CatBoostClassifier()
    model4.load_model("catboostmodel8")

    model5 = CatBoostClassifier()
    model5.load_model("catboostmodel9")

    model = CatBoostClassifier()
    model.load_model("FINALMODEL")

    get_live_data(10,time_id,match_id)
    df = pd.read_csv('Input_Data.csv') 
    df = transforming_players(df)
    df = transforming_time(df)
    df = checking_time(df)
    setting_up_training_data(df,9)
    dfs = pd.read_csv('FINAL_DF.csv') 
    dfs1 = dfs.iloc[:,1:304]
    dfs2 = dfs.iloc[:,1:486]
    dfs3 = dfs.iloc[:,1:668]
    dfs4 = dfs.iloc[:,1:850]
    dfs5 = dfs.iloc[:,1:dfs.shape[1]]

    X1 = model1.predict(dfs1,prediction_type='Probability')
    X2 = model2.predict(dfs2,prediction_type='Probability')
    X3 = model3.predict(dfs3,prediction_type='Probability')
    X4 = model4.predict(dfs4,prediction_type='Probability')
    X5 = model5.predict(dfs5,prediction_type='Probability')

    X = [X1[0][0],X2[0][0],X3[0][0],X4[0][0],X5[0][0]]
    
    print(X)

    pred_label_prob = model.predict(X,prediction_type='Probability')
    print(pred_label_prob)
    pred_label = model.predict(X)
    print(pred_label)
    return pred_label_prob,pred_label
#FINALMODEL_PREDICTION()

#FINAL MODEL PREDICTION

#x,y = setting_the_input("106926282335055885","4","6 November","13")
#print(x)
#print(y)
#FINALMODEL_PREDICTION(x,y)







