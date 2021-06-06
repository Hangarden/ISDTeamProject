from urllib.parse import urlencode, unquote, quote_plus
import requests
import pandas as pd
from pandas import json_normalize
import json


# tags = ['CORONA19_ID', 'CORONA19_DATE', 'CORONA19_NO', 'CORONA19_COUNTRY', 'CORONA19_PERSONAL', 'CORONA19_AREA', 'CORONA19_TRAVEL_HISTORY', 'CORONA19_CONTACT_HISTORY', 'CORONA19_CORRECTIVE', 'CORONA19_LEAVE_STATUS', 'CORONA19_MOVING_PATH', 'CORONA19_IDATE', 'CORONA19_MDATE']



def check_air():
    url = "http://openapi.seoul.go.kr:8088/69527972426169723130316647617062/json/Corona19Status/1/20/"
    res = requests.get(url)
    data = res.text
    info = json.loads(data)['Corona19Status']
    dfs = json_normalize(info['row'])

    return dfs

def check_air():
    url = "http://openapi.seoul.go.kr:8088/69527972426169723130316647617062/json/Corona19Status/1/20/"
    res = requests.get(url)
    data = res.text

    return dfs

def keyword(data):
    contact = data['CORONA19_CONTACT_HISTORY']

    cont_lst = []
    for i in range(len(data)):
        cont = contact.iloc[i].replace("(", " ")
        cont_lst.append(cont)

    data['CORONA19_CONTACT_HISTORY'] = cont_lst
    data.set_index('CORONA19_CONTACT_HISTORY', inplace=True)


    data.drop(index=['기타 확진자 접촉'], inplace=True)
    data.drop(index=['감염경로 조사중'], inplace=True)
    data.drop(index=['타시도 확진자 접촉'], inplace=True)
    data.drop(index=['해외유입'], inplace=True)

    data = data.drop(['CORONA19_NO', 'CORONA19_COUNTRY', 'CORONA19_PERSONAL', 'CORONA19_MOVING_PATH'], axis=1)

    data['contact'] = data.index  ## 편의상 키워드 column 추출
    contact = data['contact'].dropna()  ## null값 한 번 더 확인

    region_lst = []
    contact_lst = []
    place_lst = []
    for i in range(len(data)):

        con = contact.iloc[i].split(" ")
        region = con[0]
        contact_lst.append(con)
        region_lst.append(region)

        if str("관련") in con:
            lst_idx = con.index("관련")
            place = con[lst_idx - 1]
            place_lst.append(place)
        else:
            place_lst.append("?")

    data['contact'] = contact_lst
    data['place'] = place_lst

    data['covid_region'] = region_lst

    return data
