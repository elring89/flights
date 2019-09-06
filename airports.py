from datetime import date, timedelta
from time import sleep
import requests
from lxml import html
from geopy.geocoders import Nominatim
import json

MAX_PAGE_COUNT = 3
SLEEP_SEC_COUNT = 2

city_set = {
  'КАЗАНЬ', 'СИМФЕРОПОЛЬ', 'ЛАРНАКА', 'ЭНФИДА', 'МОСКВА(Внуково)',
  'РОСТОВ-НА-ДОНУ (ПЛАТОВ)', 'ВЕНА',
  'ХУДЖАНД', 'ЕКАТЕРИНБУРГ (Кольцово)', 'НАРЬЯН-МАР',
  'ГАЗИПАША', 'АНТАЛЬЯ', 'НОВОСИБИРСК (Толмачево)',
  'НАДЫМ', 'СОЧИ', 'ТАЛАКАН', 'МОСКВА (Шереметьево)',
  'НИЖНИЙ НОВГОРОД', 'ЯМБУРГ', 'НИЖНЕВАРТОВСК',
  'НОВЫЙ УРЕНГОЙ', 'СТАМБУЛ (Стамбул Нью)', 'НОРИЛЬСК',
  'САНЬЯ', 'БОВАНЕНКОВО', 'ДУШАНБЕ', 'КОГАЛЫМ',
  'БАРСЕЛОНА', 'СУРГУТ', 'АНАПА', 'БАКУ', 'ИЖЕВСК',
  'СЫКТЫВКАР', 'ДАЛАМАН', 'КРАСНОДАР', 'ГЕЛЕНДЖИК',
  'ИГАРКА', 'САНКТ-ПЕТЕРБУРГ (Пулково)', 'КРАСНОЯРСК',
  'МОСКВА (Домодедово)', 'ИРАКЛИОН', 'ТБИЛИСИ',
  'ТЮМЕНЬ', 'САЛЕХАРД', 'САМАРА', 'НОЯБРЬСК', 'УСИНСК',
  'ПЕРМЬ', 'ОМСК', 'ХАНТЫ-МАНСИЙСК'
}
city_info_dict = {}


def fill_city_set(days_count=7, page_count=2):
    """
    Получение данных из уфимского аэропорта из расписания (неточные данные)
    """
    today = date.today()
    city_set = set()
    for d in range(days_count):
        dt = today + timedelta(days=d)
        for p in range(1, page_count + 1):
            url = 'http://www.airportufa.ru/passazhiram/raspisanie.html?filter=1&type=1&flightNumber=0&date={0}.{1}.{2}&city=0&aircompany=0&page={3}'.format(
                dt.day, dt.month, dt.year, p
            )
            r = requests.get(url)
            tree = html.fromstring(r.text)
            el = tree.xpath('//div[@class="season-shedule_body"]/div[@class="row collapse"]/div[@class="large-3 columns"]/text()')
            for i in range(0, len(el), 2):
                # сначала город, потом авиакомпания (пропускаем)
                city_set.add(el[i])
        sleep(SLEEP_SEC_COUNT)


def get_tomorrow_schedule():
    """
    Получение расписания на завтра с сайта уфимского аэропорта
    """
    # day=2 на завтра
    url = 'http://www.airportufa.ru/regularFlight/read?day=2&operation=0&limit=0&_=1567789188346'
    geolocator = Nominatim(user_agent="elring")
    airports_dict = {}

    result = requests.get(url)
    parsed_lst = json.loads(result.content)
    for parsed in parsed_lst:
        airport_name = parsed['direction_ru']
        if airports_dict.get(airport_name):
            continue
        city_info = ''
        try:
            # убираем лишнюю инфу из скобочек
            city_name = airport_name.split('(')[0].strip()
            geo_info = geolocator.geocode(city_name, language='ru')
            city_info = geo_info.address if geo_info else ''
        except Exception as exc:
            print(exc)
        airports_dict[airport_name] = '{0} / {1}'.format(
            parsed['aircompany']['name_ru'], city_info
        )
        #print(airports_dict[airport_name])

    ad_sorted = sorted(airports_dict)
    return ' \n'.join(ad_sorted.values())


# def get_airports_info_from_wiki():
#     """
#     Получение краткого описания аэропортов с вики
#     """
#     import wikipedia
#     if not city_set:
#         fill_city_set()
#     wikipedia.set_lang('ru')
#     for city in city_set:
#         search_text = '{0} аэропорт'.format(city)
#         print(wikipedia.summary(search_text))


def get_city_info():
    """
    Получение информации о городах
    """
    if not city_set:
        fill_city_set()
    geolocator = Nominatim(user_agent="elring")
    city_list = sorted(list(city_set))
    for city in city_list:
        city_name = city.split('(')[0].strip()
        if not city_info_dict.get(city_name):
            city_info = geolocator.geocode(city_name, language='ru')
            city_info_dict[city_name] = city_info.address if city_info else ''
    city_info_list = city_info_dict.values()
    return city_info_list


def get_cities():
    fill_city_set()
    city_list = sorted(list(city_set))
    return city_list
