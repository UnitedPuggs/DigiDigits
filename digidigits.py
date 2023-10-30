import requests
import pandas as pd
from datetime import date
import aiohttp
import asyncio
import time
import sqlite3

conn = sqlite3.connect("digidigits.db")
cursor = conn.cursor()
#uses service account key to authorize sheet api
# gc = pygsheets.authorize(service_file='digikey.json')
#request to get data for all digimon cards and convert to json
allcards = requests.get("https://digimoncard.io/api-public/getAllCards.php?sort=name&series=Digimon%20Card%20Game&sortdirection=asc%27").json()

#holds the length of every request since lengths are uneven
card_amt = []

#Lists for name, number, pack, and market prices per card
card_name = []
card_num = []
card_pack = []
price_list = []
rarities = []

start = time.time()

async def get_card(session, url):
    async with session.get(url) as resp:
        digimon = await resp.json()
        return digimon

async def main(): 
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(len(allcards)):
            query = allcards[i]["cardnumber"]
            url = f'https://digimoncard.io/api/tcgplayerprices.php?cardnumber={query}'
            tasks.append(asyncio.ensure_future(get_card(session, url)))
        
        gathered_cards = await asyncio.gather(*tasks)
        for cards in gathered_cards:
            if not 'error' in cards:
                card_amt.append(len(cards))
                for i in range(len(cards)):
                    price_list.append(cards[i]['market_price'])
                    card_pack.append(cards[i]['name'])
                    rarities.append(cards[i]['rarity'])
            else: #I hate this API
                card_amt.append(0)

asyncio.run(main())
#For amount of cards in each set of data with attached names and card numbers
for i in range(len(card_amt)):
    for j in range(0, card_amt[i]):
        card_name.append(allcards[i]['name'])
        card_num.append(allcards[i]['cardnumber'])

#Creates our DataFrame and populates it with values from our lists
digi_frame = pd.DataFrame({'card_name': card_name, 'card_num': card_num, 'market_price': price_list, 'pack': card_pack, 'rarity': rarities, 'date': date.today()})
digi_frame.to_sql('marketdata', conn, if_exists='append', index=False)
#Opens Google Sheet
# sh = gc.open('DigiDigits')
#Uses the first sheet
# wks = sh[0]

#Sets data frame to cell starting at 1, 1 
# wks.set_dataframe(digi_frame, (1,1))

end = time.time() - start
print(f'{end} seconds')
conn.close()