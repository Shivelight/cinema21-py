# -*- coding: utf-8 -*-
import hmac
from random import choice
from collections import namedtuple
from uuid import uuid4
from datetime import datetime
from hashlib import md5

import requests

API = "https://mtix.21cineplex.com:2121"
WEB = "https://mtix.21cineplex.com"
HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}


class Cinema21:

    def __init__(self, uiid=None):
        self.uiid = self._generateUIID() if uiid is None else uiid

    def _getAuthKey(self):
        randId = uuid4().hex.encode()
        a_hex = md5(randId).hexdigest()
        b_hex = md5(self.uiid).hexdigest()
        date = datetime.today()
        date = "{:02d}{:02d}{:02d}".format(date.day, date.month, date.year)
        c_hex = md5(date.encode()).hexdigest()
        a_hmac = hmac.new(a_hex.encode(), b_hex.encode()).hexdigest()
        b_hmac = hmac.new(a_hmac.encode(), self.uiid).hexdigest()
        return a_hex.upper() + b_hmac.upper() + c_hex.upper()

    def _getDeviceInfo(self):
        return {
            "platform": "android",
            "uiid": self.uiid,
            "manufacturer": "samsung",
            "brand": "samsung",
            "model": "SM-A310F",
            "device_id": "universal7580",  # CPU/Chipset?
            "system_name": "Android",
            "system_version": "7.0",
            "bundle_id": "lds.cinema21",
            "build_no": 100,
            "app_version": "2.2.2",
            "read_version": "2.2.2.100",
            "device_name": "Mantra",
            "user_agent": "",
            "locale": "en-GB",
            "country": "GB",
            "time_zone": "Asia/Makassar",
            "tablet": True,
            "instant_id": "",  # App Instance ID
            "serial_number": "",  # Hardware Serial
            "carrier": "XL 4G LTE",
        }

    def _generateUIID(self):
        uuid_ = ""
        seed = "1234567890asdfghjklzxcvbnmqwertyuiop"
        for x in range(16):
                uuid_ += choice(seed)
        return uuid_.encode()

    def _post(self, data):
        data.update({
            "auth_key": self._getAuthKey(),  # Cache if hurt
            "device_uiid": self.uiid
        })
        return requests.post(API, data=data, headers=HEADERS)

    def cities(self):
        data = {
            "request_type": "list_city",
        }
        result = self._post(data).json()
        if result['status'] != 0:
            raise Cinema21Exception(result['message'])
        cities = [City(**content) for content in result['content']]
        return Cities(cities)

    def city_cinemas(self, city_id=10):
        data = {
            "request_type": "list_theater_by_city",
            "city_id": city_id,
        }
        result = self._post(data).json()
        if result['status'] != 0:
            raise Cinema21Exception(result['message'])
        return Cinemas([Cinema(**content) for content in result['premiere']],
                       [Cinema(**content) for content in result['xxi']],
                       [Cinema(**content) for content in result['imax']])

    def imax_cinemas(self):
        data = {
            "request_type": "list_theater_by_imax",
        }
        result = self._post(data).json()
        if result['status'] != 0:
            raise Cinema21Exception(result['message'])
        cinemas = [Cinema(**content) for content in result['content']]
        return Cinemas(imax=cinemas)

    def movie_cinemas(self, movie_id, city_id=10):
        data = {
            "request_type": "list_theater_by_movie",
            "city_id": city_id,
            "movie_id": movie_id,
        }
        result = self._post(data).json()
        if result['status'] != 0:
            raise Cinema21Exception(result['message'])
        return Cinemas([Cinema(**content) for content in result['premiere']],
                       [Cinema(**content) for content in result['xxi']],
                       [Cinema(**content) for content in result['imax']])

    def nearest_cinemas(self, latitude, longitude):
        data = {
            "request_type": "list_theater_nearest",
            "latitude": latitude,
            "longitude": longitude,
        }
        result = self._post(data).json()
        if result['status'] != 0:
            raise Cinema21Exception(result['message'])
        premiere = []       # type: 4
        xxi = []            # type: 2, sub_type: 0
        imax = []           # type: 2, sub_type: 1
        # can't really rely on this
        for content in result['content']:
            if content.type == 2 and content.sub_type == 0:
                xxi.append(Cinema(**content))
            elif content.type == 2 and content.sub_type == 1:
                imax.append(Cinema(**content))
            elif content.type == 4:
                premiere.append(Cinema(**content))
        return Cinemas(premiere, xxi, imax)

    def movie_schedule(self, movie_id, city_id=10):
        data = {
            "request_type": "schedule_by_movie",
            "city_id": city_id,
            "movie_id": movie_id,
        }
        result = self._post(data).json()
        if result['status'] != 0:
            raise Cinema21Exception(result['message'])
        return Cinemas([Cinema(**content) for content in result['premiere']],
                       [Cinema(**content) for content in result['xxi']],
                       [Cinema(**content) for content in result['imax']])

    def cinema_schedule(self, cinema_id, movie_id, city_id=10):
        data = {
            "request_type": "schedule_by_cinema",
            "city_id": city_id,
            "cinema_id": cinema_id,
            "movie_id": movie_id,
        }
        result = self._post(data).json()
        if result['status'] != 0:
            raise Cinema21Exception(result['message'])
        return Movie(**result['content'][0])

    def free_seat(self, cinema_id, studio_id, date_show, time_show):
        data = {
            "request_type": "get_free_seat",
            "cinema_id": cinema_id,
            "studio_id": studio_id,
            "date_show": date_show,
            "time_show": time_show
        }
        result = self._post(data).json()
        if result['status'] != 0:
            raise Cinema21Exception(result['message'])
        return result['total']

    def playing(self, city_id=10):
        data = {
            "request_type": "now_playing",
            "city_id": city_id,
        }
        result = self._post(data).json()
        if result['status'] != 0:
            raise Cinema21Exception(result['message'])
        movies = [Movie(**content) for content in result['content']]
        return Movies(movies)

    def upcoming(self, city_id=10):
        data = {
            "request_type": "coming_soon",
            "city_id": city_id,
        }
        result = self._post(data).json()
        if result['status'] != 0:
            raise Cinema21Exception(result['message'])
        movies = [Movie(**content) for content in result['content']]
        return Movies(movies)

    def version(self):
        data = {
            "request_type": "check_version",
            # "city_id": self.city_id,
        }
        result = self._post(data).json()
        return Version(result['version'])


class Cinema21Exception(Exception):
    pass


def _struct(typename, field_names):
    STRUCT = namedtuple(typename, field_names)
    STRUCT.__new__.__defaults__ = (None,) * len(STRUCT._fields)
    return STRUCT


Cinema = _struct("Cinema", ["cinema_id", "type", "sub_type", "coordinate",
                            "cinema_name", "is_mtix", "cinema_address"])
Cinemas = _struct("Cinemas", ["premiere", "xxi", "imax"])
City = _struct("City", ["city_id", "city_name"])
Cities = _struct("Cities", "cities")
Movie = _struct("Movie", ["age_limit", "can_buy", "director",
                          "distributor", "duration", "genre", "is_ats",
                          "is_mtix", "schedule", "movie_id", "movie_image",
                          "movie_type", "player", "producer", "rating",
                          "site", "synopsis", "title", "trailer", "writer"])
Movies = _struct("Movies", "movies")
# Schedule ... Shall we?
Version = _struct("Version", "version")
