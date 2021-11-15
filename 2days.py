import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
import time
from datetime import datetime
import requests
import concurrent.futures

managerName = ['papuyu','thanas','clerk','irene','evon','yggseamal','yggseathai','yggseaind']

sheetId = "1fXu7oRQoApJ0E5mg-5p1U07dWJ8lQSYVmqldK9Sx6ek"
sheetName = "AxieAccount"
headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}
index = 0
sheetURL = f"https://docs.google.com/spreadsheets/d/{sheetId}/gviz/tq?tqx=out:csv&sheet={sheetName}"
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
df = pd.read_csv(sheetURL)
df = df[['Address' , 'Manager', 'Scholar Username']]
df.set_index('Manager',inplace=True)
df = df.loc[managerName]
df.reset_index(inplace=True)
df = df[['Address']]
data = {
    "address":[],
    "total":[]
}

def slp(address):
  return(requests.get(f"https://game-api.skymavis.com/game-api/clients/{address}/items/1",headers=headers))

with concurrent.futures.ThreadPoolExecutor() as executor:
  responses = list(executor.map(slp,list(df['Address'])))

for i in range(index,df.shape[0]):
  address = df.iloc[i][0]
  #response = requests.get(f"https://game-api.skymavis.com/game-api/clients/{address}/items/1",headers=headers)
  #response = response.json()
  response = responses[i].json()
  if response['success']==True:
    total_slp = response['total']
    data["total"].append(total_slp)
    data["address"].append(address)
    index+=1

scholars = pd.DataFrame(data)
scholars=scholars.dropna()

data2= {
    "address":[],
    "total1":[],
    "total2":[]
    }
sheetId2 = "1LEdut3WTsoom03KicIRhJLvTeMnoPnIC804uUvxtwA4"
sheetURL2 = f"https://docs.google.com/spreadsheets/d/{sheetId2}/gviz/tq?tqx=out:csv&sheet={sheetName}"
df = pd.read_csv(sheetURL2)
for i in range(0,scholars.shape[0]):
  address = scholars.iloc[i][0]
  try:
    total1 = df.iloc[i][2]
  except:
    total1=0
  total2 = scholars.iloc[i][1]
  data2["address"].append(address)
  data2["total1"].append(total1)
  data2["total2"].append(total2)
scholars = pd.DataFrame(data2)



gc = gspread.service_account(filename='manager-319201-3dc4c609fd55.json')
sh = gc.open_by_key(sheetId2)
worksheet = sh.get_worksheet(0)
worksheet.clear()
set_with_dataframe(worksheet, scholars)