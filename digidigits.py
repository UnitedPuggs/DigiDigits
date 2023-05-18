import requests
import pandas as pd
import pygsheets
import aiohttp
import asyncio
import time


#uses service account key to authorize sheet api
gc = pygsheets.authorize(service_file='digikey.json')
#request to get data for all digimon cards and convert to json
allcards = requests.get("https://digimoncard.io/api-public/getAllCards.php?sort=name&series=Digimon%20Card%20Game&sortdirection=asc%27").json()

#holds the length of every request since lengths are uneven
card_amt = []

card_name = []
card_num = []
card_pack = []
price_list = []

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
            else: #I hate this API
                card_amt.append(0)

asyncio.run(main())
#For amount of cards in each set of data with attached names and card numbers
for i in range(len(card_amt)):
    for j in range(0, card_amt[i]):
        card_name.append(allcards[i]['name'])
        card_num.append(allcards[i]['cardnumber'])
#Creates our DataFrame and populates it with values from our lists
digi_frame = pd.DataFrame({'Card Names': card_name, 'Card Numbers': card_num, 'Market Price': price_list, 'Pack': card_pack})
print(digi_frame['Market Price'])
#Opens Google Sheet
sh = gc.open('DigiDigits')
#Uses the first sheet
wks = sh[0]

#Sets data frame to cell starting at 1, 1 to 1, 3
wks.set_dataframe(digi_frame, (1,1))

end = time.time() - start
print(f'{end} seconds')