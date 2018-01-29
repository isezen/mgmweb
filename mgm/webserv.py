#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from __future__ import print_function

# https://servis.mgm.gov.tr/api/merkezler/iller
# https://servis.mgm.gov.tr/api/merkezler/ililcesi?il=Izmir
# https://servis.mgm.gov.tr/api/sondurumlar?merkezid=93401
# https://servis.mgm.gov.tr/api/tahminler/gunluk?istno=93401
# https://servis.mgm.gov.tr/api/tahminler/saatlik?istno=17060
#
# https://servis.mgm.gov.tr/api/merkezler/lokasyon?enlem=38.2447&boylam=27.0849
# https://servis.mgm.gov.tr/api/merkezler?il=Izmir&ilce=Menderes


import urllib2, json

__author__ = 'ismailsezen'
__all__ = ['webserv']

class webserv(object):
    """A primitive interface to MGM web service"""

    @classmethod
    def __load(cls, url):
        return json.load(urllib2.urlopen(
            'http://servis.mgm.gov.tr/api/' + url))

    @classmethod
    def __to_ascii(cls, x):
        if isinstance(x, str): x = x.decode('utf-8')
        y = zip(list(u'ığüşçöİĞÜŞÇÖ'), list(u'iguscoIGUSCO'))
        for i, j in y: x = x.replace(i, j)
        return str(x)

    @classmethod
    def __get_province_by_plate(cls, plate):
        plates = {1: "Adana", 2: "Adıyaman", 3: "Afyon", 4: "Ağrı", \
        5: "Amasya", 6: "Ankara", 7: "Antalya", 8: "Artvin", 9: "Aydın", \
        10: "Balıkesir", 11: "Bilecik", 12: "Bingöl", 13: "Bitlis", \
        14: "Bolu", 15: "Burdur", 16: "Bursa", 17: "Çanakkale", \
        18: "Çankırı", 19: "Çorum", 20: "Denizli", 21: "Diyarbakır", \
        22: "Edirne", 23: "Elazığ", 24: "Erzincan", 25: "Erzurum", \
        26: "Eskişehir", 27: "Gaziantep", 28: "Giresun", 29: "Gümüşhane", \
        30: "Hakkari", 31: "Hatay", 32: "Isparta", 33: "İçel", \
        34: "İstanbul", 35: "İzmir", 36: "Kars", 37: "Kastamonu", \
        38: "Kayseri", 39: "Kırklareli", 40: "Kırşehir", 41: "Kocaeli", \
        42: "Konya", 43: "Kütahya", 44: "Malatya", 45: "Manisa", \
        46: "Kahramanmaraş", 47: "Mardin", 48: "Muğla", 49: "Muş", \
        50: "Nevşehir", 51: "Niğde", 52: "Ordu", 53: "Rize", \
        54: "Sakarya", 55: "Samsun", 56: "Siirt", 57: "Sinop", 58: "Sivas", \
        59: "Tekirdağ", 60: "Tokat", 61: "Trabzon", 62: "Tunceli", \
        63: "Şanlıurfa", 64: "Uşak", 65: "Van", 66: "Yozgat", \
        67: "Zonguldak", 68: "Aksaray", 69: "Bayburt", 70: "Karaman", \
        71: "Kırıkkale", 72: "Batman", 73: "Şırnak", 74: "Bartın", \
        75: "Ardahan", 76: "Iğdır", 77: "Yalova", 78: "Karabük", \
        79: "Kilis", 80: "Osmaniye", 81: "Düzce"}
        return plates[plate]

    @classmethod
    def province(cls):
        """
        Return list of provinces in Turkey

        Each province in list is stored as dict and
        contains a general information about province.
        """
        return webserv.__load('merkezler/iller')

    @classmethod
    def district(cls, province):
        province = webserv.__to_ascii(province)
        return webserv.__load('merkezler/ililcesi?il={}'.format(
            str(province)))

    @classmethod
    def latest(cls, x = 34):
        """Latest Weather Observation

        Args:
        :param x: Licence plate or id of district or station id
        """
        x = str(x)
        url = 'sondurumlar'
        if len(x) == 5:
            url += '?istno={}' if x.startswith('1') else '?merkezid={}'
        else:
            url += '/ilTumSondurum?ilPlaka={}'
        return webserv.__load(url.format(x))

    @classmethod
    def daily(cls, x, y = None):
        """Daily Forecast

        :param x: id of district or province name
        :param y: If x is province, then district name
        :type x: int or str
        :type y: str
        :rtype: dict
        """
        if y is not None:
            x = webserv.station(x, y)['merkezId']
        return webserv.__load('tahminler/gunluk?istno={}'.format(x))

    @classmethod
    def hourly(cls, x, y = None):
        if y is not None:
            x = webserv.station(x, y)['saatlikTahminIstNo']
        return webserv.__load('tahminler/saatlik?istno={}'.format(x))

    @classmethod
    def station_by_location(cls, lat, lon):
        url = 'merkezler/lokasyon?enlem={}&boylam={}'
        return webserv.__load(url.format(str(lat), str(lon)))

    @classmethod
    def station(cls, province, district):
        province = webserv.__to_ascii(province)
        district = webserv.__to_ascii(district)
        url = 'merkezler?il={}&ilce={}'
        return webserv.__load(url.format(province, district))[0]

    @classmethod
    def sta_by_plaka(cls, plaka):
        return webserv.__load('istasyonlar/il?plaka={}'.format(plaka))

