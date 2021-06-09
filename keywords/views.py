from django.shortcuts import render
from .api import related_json, confirmed_json, ranked_json
from map.models import MapCity

# 해당 구의 금일 총 확진자수와 증가된 확진자수, 관련 구 확진자수를 Mapcity에 입력.
# column을 추가해야해서 migrate 필요할 수도..?


def create(request):
    related = related_json()
    for gu in related.keys():
        city = MapCity.objects.get(sigungu_kr=gu)
        city.related_gu = related[gu]
        city.save()

    confirmed = confirmed_json()
    for gu in confirmed.keys():
        city = MapCity.objects.get(sigungu_kr=gu)
        city.accumulation = int(confirmed[gu][1])
        city.new = int(confirmed[gu][2])
        city.save()

    post = MapCity.objects.all()
    rank = ranked_json()
    context = {'post': post, 'rank': rank}
    return render(request, 'example.html', context)




