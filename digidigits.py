import requests
import pandas as pd
import pygsheets

gc = pygsheets.authorize(service_file='digikey.json')
allcards = requests.get("https://digimoncard.io/api-public/getAllCards.php?sort=name&series=Digimon%20Card%20Game&sortdirection=asc%27")
alldict = allcards.json()

data = []
lenBetweenSets = []
for i in range(0, len(alldict) - 1):
    querystring = alldict[i]["cardnumber"]
    response = requests.get(f"https://digimoncard.io/api/tcgplayerprices.php?cardnumber={querystring}")
    data += response.json()
    if "error" in data:
        data.remove("error")
    lenBetweenSets.append(len(data))
#Creates an empty dataframe
nameFrame = pd.DataFrame()
numFrame = pd.DataFrame()
priceFrame = pd.DataFrame()

cardNames = []
cardNums = []
priceList = []

for i in range(0, len(data) - 1):
    priceList.append(data[i]["market_price"])

for i in range(0, len(lenBetweenSets) - 1):
    if i == 0:
        for j in range(0, lenBetweenSets[0]):
            cardNames.append(alldict[i]["name"])
            cardNums.append(alldict[i]["cardnumber"])
    elif i > 0:
        for k in range(0, (lenBetweenSets[i] - lenBetweenSets[i - 1])):
            cardNames.append(alldict[i]["name"])
            cardNums.append(alldict[i]["cardnumber"])

nameFrame['Card Names'] = cardNames
numFrame['Card Numbers'] = cardNums
priceFrame['Market Price'] = priceList
#Creates a column for card numbers
    
sh = gc.open('DigiDigits')
wks = sh[0]

wks.set_dataframe(nameFrame,(1,1))
wks.set_dataframe(numFrame,(1,2))
wks.set_dataframe(priceFrame,(1,3))
