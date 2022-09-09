import requests
import pandas as pd
import pygsheets

#uses service account key to authorize sheet api
gc = pygsheets.authorize(service_file='digikey.json')
#request to get data for all digimon cards and convert to json
allcards = requests.get("https://digimoncard.io/api-public/getAllCards.php?sort=name&series=Digimon%20Card%20Game&sortdirection=asc%27")
alldict = allcards.json()

#data is info on every card queried from alldicts
data = []
lenBetweenSets = []
#holds the length of every request since lengths are uneven
session = requests.Session()

for i in range(len(alldict)):
    querystring = alldict[i]["cardnumber"]
    response = session.get(f"https://digimoncard.io/api/tcgplayerprices.php?cardnumber={querystring}")
    data += response.json()
    if "error" in data: #sometimes cards don't exist, so filters out errored out dicts
        data.remove("error")
    lenBetweenSets.append(len(data))

#Creates an empty dataframe
nameFrame = pd.DataFrame()
numFrame = pd.DataFrame()
priceFrame = pd.DataFrame()

#Lists for each column that will exist
cardNames = []
cardNums = []
priceList = []

for i in range(len(data)):
    priceList.append(data[i]["market_price"])

#For amount of cards in each set of data with attached names and card numbers
for i in range(len(lenBetweenSets)):
    if i == 0:
        for j in range(0, lenBetweenSets[0]):
            cardNames.append(alldict[i]["name"])
            cardNums.append(alldict[i]["cardnumber"])
    else:
        for k in range(0, (lenBetweenSets[i] - lenBetweenSets[i - 1])):
            cardNames.append(alldict[i]["name"])
            cardNums.append(alldict[i]["cardnumber"])

#Creates the columns
nameFrame['Card Names'] = cardNames
numFrame['Card Numbers'] = cardNums
priceFrame['Market Price'] = priceList
    
#Opens Google Sheet
sh = gc.open('DigiDigits')
#Uses the first sheet
wks = sh[0]

#Sets data frame to cell starting at 1, 1 to 1, 3
wks.set_dataframe(nameFrame,(1,1))
wks.set_dataframe(numFrame,(1,2))
wks.set_dataframe(priceFrame,(1,3))
