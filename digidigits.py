import requests
#import pandas as pd

allcards = requests.get("https://digimoncard.io/api-public/getAllCards.php?sort=name&series=Digimon%20Card%20Game&sortdirection=asc%27")
alldicts = allcards.json()
url = "https://digimoncard.io/api/tcgplayerprices.php"

data = []
for i in range(0, len(alldicts) - 1):
    querystring = alldicts[i]["cardnumber"]
    response = requests.get(f"https://digimoncard.io/api/tcgplayerprices.php?cardnumber={querystring}")
    data += response.json()

price = data[0]["market_price"]
card = alldicts[0]["cardnumber"]

print(f"Price for index 0 is {price} and card number is {card}")