import requests
from igdb.wrapper import IGDBWrapper
import json
import time
from google.colab import auth
import gspread
from google.auth import default
import pandas as pd

def makeItem(jason):
  game = jason.split('\n')
  return game

auth.authenticate_user()
creds, _ = default()

gc = gspread.authorize(creds)

worksheet = gc.open('ID_INPUT').sheet1
IDlist = []
# get_all_values gives a list of rows.
rows = worksheet.get_all_values()
for x in rows:
  IDlist.append(x[0])
  
  getToken = requests.post("https://id.twitch.tv/oauth2/token?client_id= IDHERE &client_secret= SECRETHERE &grant_type=client_credentials")
s = getToken.text
sI = s.split("\"")
accessToken = sI[3]
accessID = "YOUR ACCESS ID"
wrapper = IGDBWrapper(accessID, accessToken)
games = []
for ID in IDlist:
  rq = 'fields name, age_ratings, category, cover, first_release_date, genres, involved_companies, summary, themes, url; where id = ' + ID + ';'
  byteArray = wrapper.api_request(
              'games',
              rq
            )
  myJson = byteArray.decode('utf8').replace("'", '"')
  games.append(makeItem(myJson))
  time.sleep(.1)

display(games)
# pd.DataFrame.from_records(games)
