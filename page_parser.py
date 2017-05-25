# -*- coding: utf-8 -*-

from lxml import html, etree
from HTMLParser import HTMLParser
import json


class PageParser:
    def __init__(self, page_id, page_str):
        self.__html_parser = HTMLParser()
        self.__tree = html.fromstring(page_str)
        self.__details_elem = None
        self.__page_id = page_id

    def is_valid(self):
        self.__details_elem = self.__tree.xpath('//table[@id="details"]')
        return len(self.__details_elem) > 0

    def parse(self):
        title = self.__tree.xpath('//div/h1/text()')[0]
        info = self.__get_info()

        category = info[u'Категория'].xpath('./a/text()')[0]
        size = info[u'Размер'].xpath('text()')[0]
        added = info[u'Добавлен'].xpath('text()')[0]

        torrent_info = TorrentInfo(self.__page_id, title, category, size, added)

        return torrent_info

    def __get_info(self):
        result = {}
        elems = self.__details_elem[0].xpath('.//tr')

        for i, item in enumerate(elems):
            nested_elem = item.xpath('./td[@class = "header"]/text()')

            if len(nested_elem) > 0:
                key = nested_elem[0]
                value = item.xpath('./td')[1]

                result[key] = value

        return result

class TorrentInfo:
    def __init__(self, torrent_id, title, category, size, added):
        self.torrent_id = torrent_id
        self.title = title
        self.category = category
        self.size = size
        self.added = added

    def to_json(self):
        dict = {'torrent_id': self.torrent_id, 'title': self.title, 'category': self.category, 'size': self.size, 'added': self.added}
        return json.dumps(dict, ensure_ascii=False)
