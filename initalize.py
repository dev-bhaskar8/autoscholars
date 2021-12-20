import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
import time
from datetime import datetime
import requests
import concurrent.futures


managerName = ['bhaskar']

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
data1 = {
    "address":[],
    "total1":[],
    "total2":[]
}
data2 = {
  "addresses":[],
}
now = str(time.time())
data2[now]=[]

def slp(address):
  return(requests.get(f"https://game-api.skymavis.com/game-api/clients/{address}/items/1",headers=headers))

with concurrent.futures.ThreadPoolExecutor() as executor:
  responses = list(executor.map(slp,list(df['Address'])))

for i in range(index,df.shape[0]):
  address = df.iloc[i][0]
  response = responses[i].json()
  if response['success']==True:
    total_slp = response['total']
    data1["total1"].append(total_slp)
    data1["total2"].append(total_slp)
    data1["address"].append(address)
    data2["addresses"].append(address)
    data2[now].append(0)
    index+=1

two_days = pd.DataFrame(data1)
two_days = two_days.dropna()
logs = pd.DataFrame(data2)
logs = logs.dropna()

sheetId2 = "1h-dRUU2LDgbmWSl7vFsY7aFq7ryguYMFTpQgv2kJ_n8"

gc = gspread.service_account(filename='manager-319201-3dc4c609fd55.json')
sh = gc.open_by_key(sheetId2)
worksheet = sh.get_worksheet(0)
worksheet.clear()
set_with_dataframe(worksheet, two_days)
worksheet = sh.get_worksheet(1)
worksheet.clear()
set_with_dataframe(worksheet, logs)
