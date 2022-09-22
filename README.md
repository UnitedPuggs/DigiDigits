# DigiDigits
Python script that utilizes API calls for monetary comparisons as market prices for each individual cards shift. The end goal is to be able to find the greater positive and negative changes in market price. Using Digimoncard.io's API to grab a .json of all current Digimon cards, assigning it to a list of dicts, and then looping through that list and querying the digimoncard.io API for .json files of each individual card and selecting that card's name, number, and current market price. This data is all parsed and populates a Google Sheet by using Google Sheets + Drive API and the pandas module.

## A look at the data sheet
![sheet](https://github.com/UnitedPuggs/DigiDigits/blob/main/DigiSheet.png)

## Idea for the final product
![concept](https://github.com/UnitedPuggs/DigiDigits/blob/main/DigiConcept.png)
