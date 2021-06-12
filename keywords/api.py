from urllib.parse import urlencode, unquote, quote_plus
import requests
import pandas as pd
from pandas import json_normalize
import json
import collections
import itertools


# 관련구 json_data
def x_json():
    url = "http://openapi.seoul.go.kr:8088/69527972426169723130316647617062/json/Corona19Status/1/1000"
    res = requests.get(url)
    data = res.text
    info = json.loads(data)['Corona19Status']
    covid = json_normalize(info['row'])

    contact = covid['CORONA19_CONTACT_HISTORY']

    cont_lst = []
    for i in range(len(covid)):
        cont = contact.iloc[i].replace("(", " ")
        cont_lst.append(cont)

    covid['CORONA19_CONTACT_HISTORY'] = cont_lst

    covid.set_index('CORONA19_CONTACT_HISTORY', inplace=True)

    covid.drop(index=['기타 확진자 접촉'], inplace=True)
    covid.drop(index=['감염경로 조사중'], inplace=True)
    covid.drop(index=['타시도 확진자 접촉'], inplace=True)
    covid.drop(index=['해외유입'], inplace=True)

    covid = covid.drop(['CORONA19_NO', 'CORONA19_COUNTRY', 'CORONA19_PERSONAL', 'CORONA19_MOVING_PATH'], axis=1)

    covid['contact'] = covid.index  ## 편의상 키워드 column 추출
    contact = covid['contact'].dropna()  ## null값 한 번 더 확인

    region_lst = []
    contact_lst = []
    place_lst = []
    for i in range(len(covid)):

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

    covid['contact'] = contact_lst
    covid['place'] = place_lst

    covid['covid_region'] = region_lst

    return covid

def all_json():
    url = "http://openapi.seoul.go.kr:8088/69527972426169723130316647617062/json/Corona19Status/1/1000"
    res = requests.get(url)
    data = res.text
    info = json.loads(data)['Corona19Status']
    covid = json_normalize(info['row'])

    for i in range(1, 45):
        url = "http://openapi.seoul.go.kr:8088/69527972426169723130316647617062/json/Corona19Status/{0}/{1}".format(
            1000 * i + 1, 1000 * i + 1000)
        res = requests.get(url)
        data = res.text
        info = json.loads(data)['Corona19Status']
        new = json_normalize(info['row'])
        covid = pd.concat([covid, new])

    contact = covid['CORONA19_CONTACT_HISTORY']

    cont_lst = []
    for i in range(len(covid)):
        cont = contact.iloc[i].replace("(", " ")
        cont_lst.append(cont)

    covid['CORONA19_CONTACT_HISTORY'] = cont_lst

    covid.set_index('CORONA19_CONTACT_HISTORY', inplace=True)

    covid.drop(index=['기타 확진자 접촉'], inplace=True)
    covid.drop(index=['감염경로 조사중'], inplace=True)
    covid.drop(index=['타시도 확진자 접촉'], inplace=True)
    covid.drop(index=['해외유입'], inplace=True)

    covid = covid.drop(['CORONA19_NO', 'CORONA19_COUNTRY', 'CORONA19_PERSONAL', 'CORONA19_MOVING_PATH'], axis=1)

    covid['contact'] = covid.index  ## 편의상 키워드 column 추출
    contact = covid['contact'].dropna()  ## null값 한 번 더 확인

    region_lst = []
    contact_lst = []
    place_lst = []
    for i in range(len(covid)):

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

    covid['contact'] = contact_lst
    covid['place'] = place_lst

    covid['covid_region'] = region_lst

    return covid

def related_json(covid):

    cityList = {}
    cities = ['강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구', '노원구', '도봉구', '동대문구', '동작구', '마포구', '서대문구', '서초구',
              '성동구', '성북구', '송파구', '양천구', '영등포구', '용산구', '은평구', '종로구', '중구', '중랑구']
    for city in cities:
        series = pd.Series(covid[covid['covid_region'] == city]['CORONA19_AREA'].value_counts(), dtype='float')
        a = dict(series)

        try:
            if a['타시도'] >= 1:
                a.pop('타시도')
        except:
            pass

        try:
            if a['기타'] >= 1:
                a.pop('기타')
        except:
            pass
        try:
            if a[city] >= 1:
                a.pop(city)
        except:
            pass

        cityList[city] = a

    return cityList


def confirmed_json():
    url = "http://openapi.seoul.go.kr:8088/587671694b6169723631477470454d/json/TbCorona19CountStatusJCG/1/1"
    res = requests.get(url)
    data = res.text
    info = json.loads(data)['TbCorona19CountStatusJCG']['row']

    cities = ['종로구', '중구', '용산구', '성동구', '광진구', '동대문구', '중랑구', '성북구', '강북구', '도봉구', '노원구', '은평구', '서대문구', '마포구', '양천구',
              '강서구', '구로구', '금천구', '영등포구', '동작구', '관악구', '서초구', '강남구', '송파구', '강동구']

    dicts = dict()

    for i in range(0, len(cities)):
        dicts[cities[i]] = [list(info[0].values())[0], list(info[0].values())[2*i+1], list(info[0].values())[2*i+2]]

    return dicts

def ranked_json(covid):
    cities = ['강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구', '노원구', '도봉구', '동대문구', '동작구', '마포구', '서대문구', '서초구',
              '성동구', '성북구', '송파구', '양천구', '영등포구', '용산구', '은평구', '종로구', '중구', '중랑구']

    lists = {}

    for city in cities:
        x_gu = covid[covid['covid_region'] == city]
        x_dict = collections.Counter(itertools.chain.from_iterable(str(k).split(',') for k in x_gu['place']))
        x_dict_sorted = dict(sorted(x_dict.items(), key=(lambda x: x[1]), reverse=True))
        x_dict_sorted = {key: val for key, val in x_dict_sorted.items() if val <= 800}
        x_df = pd.DataFrame()
        x_df['Word'] = x_dict_sorted.keys()
        x_df['Frequency'] = x_dict_sorted.values()

        words = x_df.Word.to_list()
        frequencies = x_df.Frequency.to_list()

        lists[city] = {}
        for i in range(len(words)):
            if words[i] == '?':
                continue
            lists[city][words[i]] = frequencies[i]

    return lists