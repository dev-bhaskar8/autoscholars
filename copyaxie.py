import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
import time
from datetime import datetime
import requests

sheetId = "1fXu7oRQoApJ0E5mg-5p1U07dWJ8lQSYVmqldK9Sx6ek"
sheetId2 = "1LEdut3WTsoom03KicIRhJLvTeMnoPnIC804uUvxtwA4"
sheetName = "AxieAccount"
sheetURL = f"https://docs.google.com/spreadsheets/d/{sheetId}/gviz/tq?tqx=out:csv&sheet={sheetName}"
pd.options.display.float_format = '{:.0f}'.format
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
scholars = pd.read_csv(sheetURL)
gc = gspread.service_account(filename='manager-319201-3dc4c609fd55.json')
sh = gc.open_by_key(sheetId2)
worksheet = sh.get_worksheet(2)
worksheet.clear()
set_with_dataframe(worksheet, scholars)