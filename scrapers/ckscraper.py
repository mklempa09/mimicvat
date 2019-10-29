from splinter import Browser
import sqlite3
import urllib.request
from bs4 import BeautifulSoup as b


# this gets all mythics from som and creates a list of them

# sqlite query all mythics
# for line in query, add to list
# for object in list, pop to another list up to 500
# for object in another list, 





html = urllib.request.urlopen(url).read()
soup = b(html, 'html.parser')
cardsDb = sqlite3.connect('CARDINFO.db')
c = cardsDb.cursor()

# sql collect info, adds to cList
cList = []
try:
    # connects db, fills cList with ALL mythics and rares

    for x in c.execute('select name, cardset from cards where rarity = "mythic"'):
        innerList = '"'+x[0]+'",'+x[1]+',0,1 \n'
        cList.append(innerList)
except:
    print('could not write sql function')
#or x in cList:
#    print(x)
cardsDb.close()

# pasteVal is the string that gets inserted to the browser with 500 values of cards


# converts cList into 500 long chunks, then returns that chunk as popList and passes it to pasteHtml
#
def selectRows(cList):
    while len(cList) != 0:
        print('clist is not zero')
        popList = []
        #for i in range(0,500):
        for i in range(0,20):
            if len(cList) == 0:
                # this means the cList is empty, everything has been pop'd
                print('breaking popList append')
                break
            else:
                popList.append(cList.pop(0))
                print('appending popList')
        print('range loop finished, poplist length should be 20')
        print('poplist len:',len(popList))
        # the loop counts up items and finishes here. I should call the function to run the chrome sim here
        pasteHtml(popList)
        #print(popList)
        #pasteVal = popList
        #return pasteVal
    print('clist is at zero')

# cList = selectRows(cList)
# starts the chrome environment, creates the pasteVal with popList, passes it to the browser and submits
def pasteHtml(popList):

    executable_path = {'executable_path' :r'C:\Users\Tim\Desktop\chrome\chromedriver'}

    browser = Browser('chrome', **executable_path, headless = False)
    browser.visit(r"https://www.cardkingdom.com/static/csvImport")

    pasteVal = ''

    for x in popList:
        pasteVal = pasteVal + x

    # htmlId is, naturally, the ID value of the tag that I'm looking to paste into
    # here, I fill the html text box with my pasteVal, then hit the submit button
    htmlId = r"csvPaste"
    pasteBox = browser.find_by_id(htmlId)
    pasteBox.fill(pasteVal)

    submitId = r"convertPastedCsv"
    submit = browser.find_by_id(submitId).first.click()

# selectRows(cList)
#"""
# google test

"""
with Browser() as browser:
    # Visit URL
    url = "http://www.google.com"
    browser.visit(url)
"""
"""
# scrape function
def ck_scrape():

    for line in csv:
        # append a list of lists
        None

    pasteBox = browser.find_by_id(htmlId)
    pasteBox.fill(pasteVal)

    submitId = "convertPastedCsv"
    submit = browser.find_by_id(submitId).first.click()
"""

# print('this should do nothing')

selectRows(cList)