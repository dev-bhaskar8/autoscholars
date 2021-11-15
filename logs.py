import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
import time
from datetime import datetime
import requests

sheetId2 = "1LEdut3WTsoom03KicIRhJLvTeMnoPnIC804uUvxtwA4"
sheetURL2 = f"https://docs.google.com/spreadsheets/d/{sheetId2}/gviz/tq?tqx=out:csv&sheet"
sheetURL3 = f"https://docs.google.com/spreadsheets/d/{sheetId2}/gviz/tq?tqx=out:csv&sheet=logs"
scholars = pd.read_csv(sheetURL2)
logs = pd.read_csv(sheetURL3)
logs.dropna(axis=1,inplace=True)
cols = list(logs.columns.values)
cols.pop(cols.index('addresses'))
data2= {
    "addresses":[],
    }
for col in cols:
  data2[col]=[]
for i in range(0,scholars.shape[0]):
  addresses= scholars.iloc[i][0]
  for col in cols:
    try:
      a = logs.iloc[i].loc[col]
    except:
      a = 0
    data2[col].append(a)
  data2['addresses'].append(addresses)
logs = pd.DataFrame(data2)
logs[time.time()] = scholars['total2']-scholars['total1']


gc = gspread.service_account(filename='manager-319201-3dc4c609fd55.json')
sh = gc.open_by_key(sheetId2)
worksheet = sh.get_worksheet(1)
worksheet.clear()
set_with_dataframe(worksheet, logs)