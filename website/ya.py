from log import logger
from requests import get
import json
import random
import datetime
from os import path, mkdir

API_KEY = ""
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


def get_ticket(from_st, to_st, date):
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
    if "pagination" in tickets:
        total = tickets["pagination"]["total"]
        if total:
            best = tickets["segments"][random.randint(0, total-1)]
            arrival = datetime.datetime.strptime(best["arrival"], "%Y-%m-%dT%H:%M:%S+03:00")
            departure = datetime.datetime.strptime(best["departure"], "%Y-%m-%dT%H:%M:%S+03:00")
            delta = arrival - departure
            from_title = best["from"]["title"]
            to_title = best["to"]["title"]
            carrier = best["thread"]["carrier"]["title"]
            return {"departure_hour": departure.hour,
                    "departure_minute": departure.minute,
                    "flight_hour": delta.seconds//3600,
                    "flight_minute":(delta.seconds % 3600)//60,
                    "from_title": from_title,
                    "to_title": to_title,
                    "carrier": carrier,
                    "cost": random.randint(20, 60) * 100,
                    "status": True
                    }
    return {"status": False}


def find_ticket(from_station, to_station, date):
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
        return get_ticket(from_st_, to_st_, date)
    return {"status": False}


if __name__ == "__main__":
    print(find_ticket("москва", "ухта", "2020-3-22"))