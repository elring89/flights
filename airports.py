from datetime import date, timedelta
from time import sleep
import requests
from lxml import html
from geopy.geocoders import Nominatim
#import wikipedia

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
    Получение данных из уфимского аэропорта
    """
    print('Запрос в аэропорт')
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


# def get_airports_info_from_wiki():
#     """
#     Получение краткого описания аэропортов с вики
#     """
#     if not city_set:
#         fill_city_set()
#     wikipedia.set_lang("ru")
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
    for city in city_set:
        city_name = city.split('(')[0].strip()
        if not city_info_dict.get(city_name):
            city_info = (geolocator.geocode(city_name, language='ru'))
            city_info_dict[city_name] = city_info
    return city_info_dict.values()


def get_cities():
    if not city_set:
        fill_city_set()
    return list(city_set)
