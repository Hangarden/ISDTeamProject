from urllib.parse import urlencode, unquote, quote_plus
import requests
import pandas as pd
from pandas import json_normalize
import json






def check_air():
    url2 = "http://openapi.seoul.go.kr:8088/69527972426169723130316647617062/json/Corona19Status/1/1000/"
    res2 = requests.get(url2)
    data2 = res2.text
    info2 = json.loads(data2)['Corona19Status']
    covid = json_normalize(info2['row'])

    contact = covid['CORONA19_CONTACT_HISTORY']

    cont_lst = []
    for i in range(len(covid)):
        cont = contact.iloc[i].replace("(", " ")
        cont_lst.append(cont)

    covid['CORONA19_CONTACT_HISTORY'] = cont_lst

    covid.set_index('CORONA19_CONTACT_HISTORY', inplace=True)  ## 주로 언론사 활용 --> 언론사를 인덱스로

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

    cityList = {}
    cities = ['강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구', '노원구', '도봉구', '동대문구', '동작구', '마포구', '서대문구', '서초구',
              '성동구', '성북구', '송파구', '양천구', '영등포구', '용산구', '은평구', '종로구', '중구', '중랑구']
    for city in cities:
        series = pd.Series(covid[covid['covid_region'] == city]['CORONA19_AREA'].value_counts(), dtype='int32')
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

        cityList_df = pd.DataFrame.from_dict(cityList, orient='index')
        result = cityList_df.to_json(orient='columns')
        parsed = json.loads(result)
        b = json.dumps(parsed, indent=4, ensure_ascii=False)

        print(b)

