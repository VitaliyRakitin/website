from log import logger
from requests import get
import json
import random
import datetime
from os import path, mkdir

API_KEY = "6f7d84fe-ded9-4d18-a300-52b496dfc03a"
YDX_PATH = "https://api.rasp.yandex.net/v3.0/search/"
resp_format = "json"
lang = "ru_RU"
page = 1
RESOURCES_PATH = "resources"
DATA_PATH = RESOURCES_PATH + "/data.json"


def get_codes():
    def get_ya_rasp():
        return get(
            "https://api.rasp.yandex.net/v3.0/stations_list/",
            params={
                "apikey": API_KEY,
                "lang": lang,
                "format": resp_format
            }
        ).json()

    def parse_ya_rasp(data):
        codes = []
        for country in data["countries"]:
            for region in country["regions"]:
                for settlement in region["settlements"]:
                    if "yandex_code" in settlement["codes"]:
                        codes_local = {
                            "code": settlement["codes"]["yandex_code"],
                            "title": settlement["title"].lower(),
                            "airports": [station["title"].lower() for station in settlement["stations"] if
                                         station["station_type"] == "airport"]
                        }
                        if len(codes_local["airports"]):
                            codes.append(codes_local)
        return codes

    if path.exists(DATA_PATH):
        with open(DATA_PATH, 'r') as f:
            data = json.load(f)
    else:
        data = parse_ya_rasp(get_ya_rasp())
        mkdir(RESOURCES_PATH)
        with open(DATA_PATH, 'w') as f:
            json.dump(data, f)

    return data


def parse_tickets(tickets, amount=1):
    tickets_parsed = []
    if "pagination" in tickets:
        total = tickets["pagination"]["total"]
        sample = random.sample(tickets["segments"], amount if amount < total else total)
        for best in sample:
            print(best)
            arrival = datetime.datetime.fromisoformat(best["arrival"])
            departure = datetime.datetime.fromisoformat(best["departure"])
            delta = arrival - departure
            from_title = best["from"]["title"]
            to_title = best["to"]["title"]
            carrier = best["thread"]["carrier"]["title"]
            tickets_parsed.append({
                "departure_hour": departure.hour,
                "departure_minute": departure.minute,
                "flight_hour": delta.seconds//3600,
                "flight_minute": (delta.seconds % 3600)//60,
                "from_title": from_title,
                "to_title": to_title,
                "carrier": carrier,
                "cost": random.randint(20, 60) * 100,
                "status": True
            })
    return {"status": True if tickets_parsed else False, "tickets": tickets_parsed}


def get_ticket(from_st, to_st, date, amount=1):
    def get_ya_rasp(from_st, to_st, date):
        return get(
            "https://api.rasp.yandex.net/v3.0/search/",
            params={
                "apikey": API_KEY,
                "format": resp_format,
                "lang": lang,
                "page": page,
                "from": from_st,
                "to": to_st,
                "date": date,
                "transport_types": "plane"
            }
        ).json()

    tickets = get_ya_rasp(from_st, to_st, date)
    return parse_tickets(tickets, amount)


def find_ticket(from_station, to_station, date, amount=1):
    def get_station(city):
        city = city[:-1]
        codes = get_codes()
        for item in codes:
            if city in item["title"] or any(city in airport for airport in item["airports"]):
                return item["code"]
        return None

    from_st_ = get_station(from_station.lower())
    to_st_ = get_station(to_station.lower())
    logger.info("TRANSFORM FORM: {0}:{1}".format(from_station, from_st_))
    logger.info("TRANSFORM TO: {0}:{1}".format(to_station, to_st_))

    if from_st_ and to_st_:
        return get_ticket(from_st_, to_st_, date, amount)
    return {"status": False}


if __name__ == "__main__":
    print(find_ticket("москва", "сочи", "2020-3-22", 3))
    data = {"pagination": {"total": 1}, "segments":[{'arrival': '2020-03-23T06:05:00+07:00', 'from': {'code': 's9600215', 'title': 'Внуково', 'station_type': 'airport', 'popular_title': '', 'short_title': '', 'transport_type': 'plane', 'station_type_name': 'аэропорт', 'type': 'station'}, 'thread': {'uid': '7R-4571_1_c96_547', 'title': 'Москва — Красноярск', 'number': '7R 4571', 'short_title': 'Москва — Красноярск', 'thread_method_link': 'api.rasp.yandex.net/v3/thread/?date=2020-03-22&uid=7R-4571_1_c96_547', 'carrier': {'code': 96, 'contacts': 'Телефон круглосуточного контактного центра для бронирования и информации: 8 800 5555 800 (звонок по России бесплатный)\r\n\r\nТелефоны: <br>\r\nприёмная: +7 (495) 663-77-53;<br>\r\nслужба организации регулярных перевозок: (495) 662-38-52;<br>\r\nкасса: +7 (495) 641-10-66', 'url': 'http://www.rusline.aero/', 'logo_svg': '//yastat.net/s3/rasp/media/data/company/svg/rusline.svg', 'title': 'РусЛайн', 'phone': '', 'codes': {'icao': 'RLU', 'sirena': 'РГ', 'iata': '7R'}, 'address': 'г. Москва, ул. Ленинская слобода, д.19, бизнес-центр «Омега Плаза»', 'logo': '//yastat.net/s3/rasp/media/data/company/logo/Rusline.jpg', 'email': 'sop@rusline.aero'}, 'transport_type': 'plane', 'vehicle': 'Boeing 737-800', 'transport_subtype': {'color': None, 'code': None, 'title': None}, 'express_type': None}, 'departure_platform': '', 'departure': '2020-03-22T21:20:00+03:00', 'stops': '', 'departure_terminal': None, 'to': {'code': 's9600376', 'title': 'Емельяново', 'station_type': 'airport', 'popular_title': '', 'short_title': '', 'transport_type': 'plane', 'station_type_name': 'аэропорт', 'type': 'station'}, 'has_transfers': False, 'tickets_info': {'et_marker': False, 'places': []}, 'duration': 17100.0, 'arrival_terminal': None, 'start_date': '2020-03-22', 'arrival_platform': ''}]}
    # arrival = datetime.datetime.fromisoformat(best["arrival"])
    # departure = datetime.datetime.fromisoformat(best["departure"])
    # print(parse_tickets(data, 12))