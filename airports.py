from datetime import date, timedelta
from time import sleep
import requests
from lxml import html
from geopy.geocoders import Nominatim
import json

MAX_PAGE_COUNT = 3
SLEEP_SEC_COUNT = 2
UFA_AIRPORT_URL = 'http://www.airportufa.ru/'

# city_set = {
#   'КАЗАНЬ', 'СИМФЕРОПОЛЬ', 'ЛАРНАКА', 'ЭНФИДА', 'МОСКВА(Внуково)',
#   'РОСТОВ-НА-ДОНУ (ПЛАТОВ)', 'ВЕНА',
#   'ХУДЖАНД', 'ЕКАТЕРИНБУРГ (Кольцово)', 'НАРЬЯН-МАР',
#   'ГАЗИПАША', 'АНТАЛЬЯ', 'НОВОСИБИРСК (Толмачево)',
#   'НАДЫМ', 'СОЧИ', 'ТАЛАКАН', 'МОСКВА (Шереметьево)',
#   'НИЖНИЙ НОВГОРОД', 'ЯМБУРГ', 'НИЖНЕВАРТОВСК',
#   'НОВЫЙ УРЕНГОЙ', 'СТАМБУЛ (Стамбул Нью)', 'НОРИЛЬСК',
#   'САНЬЯ', 'БОВАНЕНКОВО', 'ДУШАНБЕ', 'КОГАЛЫМ',
#   'БАРСЕЛОНА', 'СУРГУТ', 'АНАПА', 'БАКУ', 'ИЖЕВСК',
#   'СЫКТЫВКАР', 'ДАЛАМАН', 'КРАСНОДАР', 'ГЕЛЕНДЖИК',
#   'ИГАРКА', 'САНКТ-ПЕТЕРБУРГ (Пулково)', 'КРАСНОЯРСК',
#   'МОСКВА (Домодедово)', 'ИРАКЛИОН', 'ТБИЛИСИ',
#   'ТЮМЕНЬ', 'САЛЕХАРД', 'САМАРА', 'НОЯБРЬСК', 'УСИНСК',
#   'ПЕРМЬ', 'ОМСК', 'ХАНТЫ-МАНСИЙСК'
# }

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

def get_city_set(days_count=7, page_count=2):
    """
    Получение данных из уфимского аэропорта из расписания (неточные данные)
    """
    today = date.today()
    city_set = set()
    for d in range(days_count):
        dt = today + timedelta(days=d)
        for p in range(1, page_count + 1):
            url = '{0}passazhiram/raspisanie.html?filter=1&type=1&flightNumber=0&date={1}.{2}.{3}&city=0&aircompany=0&page={4}'.format(
                UFA_AIRPORT_URL, dt.day, dt.month, dt.year, p
            )
            r = requests.get(url)
            tree = html.fromstring(r.text)
            el = tree.xpath('//div[@class="season-shedule_body"]/div[@class="row collapse"]/div[@class="large-3 columns"]/text()')
            for i in range(0, len(el), 2):
                # сначала город, потом авиакомпания (пропускаем)
                city_set.add(el[i])
        sleep(SLEEP_SEC_COUNT)
    return city_set


class UfaAirport():
    def __init__(self):
        self.directions = {}
        self.last_dt = None

    def get_address(self, direction):
        geolocator = Nominatim(user_agent="elring")
        address = ''
        try:
            # убираем лишнюю инфу из скобочек
            city_name = direction.split('(')[0].strip()
            geo = geolocator.geocode(city_name, language='ru')
            address = geo.address if geo else ''
        except Exception as exc:
            print(exc)
        return address

    def fill_directions(self):
        # day=2 на завтра
        url = '{0}regularFlight/read?day={1}&operation=0&limit=0&_=1567789188346'.format(
            UFA_AIRPORT_URL, 2)
        print('Обращение в аэропорт')
        result = requests.get(url)
        parsed_result = json.loads(result.content)
        for parsed in parsed_result:
            direction = parsed['direction_ru']
            if self.directions.get(direction):
                continue
            address = self.get_address(direction)
            self.directions[direction] = '{0} / {1}'.format(
                parsed['aircompany']['name_ru'], address)
        # запоним сегодняшнюю дату
        self.last_dt = date.today()

    def get_schedule_msg(self):
        today = date.today()
        if not self.last_dt or self.last_dt < today:
            # заполняем раз в день
            self.fill_directions()

        schedule_msg = ''
        sorted_keys = sorted(self.directions.keys())
        for k in sorted_keys:
            schedule_msg += self.directions[k] + ' \n'
        return schedule_msg

UA = UfaAirport()
msg = UA.get_schedule_msg()
print(msg)
msg = UA.get_schedule_msg()
print(msg)
