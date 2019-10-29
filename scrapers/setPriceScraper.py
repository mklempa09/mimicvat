import urllib.request
import json
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import csv
import time
import datetime
import sqlite3
import sys



#functions:

def dataParse():
    for obj in data['data']:
        print(obj['name'])
        print(obj['prices']['usd'])
        print(obj['id'])

def checkPage(data):
    try:
        if data['has_more'] == True:
            #print(obj['has_more'])
                print('I found another page of cards')
                #do an addCards with obj['next_page']
                #print('the next page url:',data['next_page'])
                jason_obj = urllib.request.urlopen(data['next_page'])
                data = json.load(jason_obj)
                dailyPrice(data)
    except:
        print('check page could not perform loop')

def setGeneration(set):
    print('the set is',set)
    url = "https://api.scryfall.com/cards/search?q=set%3D" + set
    print('sleeping now')
    time.sleep(.600)
    print('the url is',url)
    try:
        jason_obj = urllib.request.urlopen(url)
        data = json.load(jason_obj)
        dailyPrice(data)
    except:
        print('something went wrong with set',set)

#gets the datetime
def getTime():
        try:
                ts = time.time()
                dateTime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                return dateTime
        except:
                print('getTime didnt work')
print('test getTime:',getTime())

def foilRatio():
        try:
                foilRatio = float(obj['prices']['usd_foil'])/float(obj['prices']['usd'])
                return foilRatio
        except:
                return None

def dailyPrice(data):
    for obj in data['data']:
        #print('obj name:',obj['name'])
        foilCalc = None
        usd = None
        foilUsd = None
        if obj['prices']['usd_foil'] == None:
                None
        else:
                foilUsd = obj['prices']['usd_foil']
        if obj['prices']['usd_foil'] == None or obj['prices']['usd']==None:
                foilCalc = None
        else:
                foilCalc = float(obj['prices']['usd_foil'])/float(obj['prices']['usd'])
        #print('foil:',obj['prices']['usd_foil'])
        #print('usd:',obj['prices']['usd'])

        #print(float(obj['prices']['usd_foil'])/float(obj['prices']['usd']))
        try:
                c.execute('insert into PRICES values (?,?,?,?,?)',(
                obj['id'],
                getTime(),
                obj['prices']['usd'],
                obj['prices']['usd_foil'],
                foilCalc
                ))
        except:
                print('could not add to db')
                print( 'id:', obj['id'],'usd:' ,obj['prices']['usd'], 'foil:', obj['prices']['usd_foil'])
                sys.exit()
    checkPage(data)
def printDb():
        print('im printing the db here:')
        for row in c.execute('SELECT * FROM PRICES'):
                print(row)




#connecting to db (this should probably be inside the dailyPrice loop to allow the commit and close functions)
cardsDb = sqlite3.connect('CARDINFO.db')
c = cardsDb.cursor()


#this opens the set names, and adds the values to the database for all cards found in all sets
with open('setNames.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for line in csv_reader:
        print('set scraping:',line[0])
        setGeneration(line[0])
        
        #return line[0]             can't return outside of a function




cardsDb.commit()
#printDb()
print('im closing the db')
cardsDb.close()