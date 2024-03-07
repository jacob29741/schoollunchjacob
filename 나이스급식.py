import requests
import json

url="https://open.neis.go.kr/hub/mealServiceDietInfo"

key="3eac55ceb9504041ac74bfcfb016f888"

params = {
    'KEY' : key,
    'Type' : 'json',
    'pIndex' : '1',
    'ATPT_OFCDC_SC_CODE' : 'S10',
    'SD_SCHUL_CODE' : '9010462',
    'MLSV_YMD' : '20240305'
}

requests = requests.get(url, params=params)

contents = requests.text
print(contents)