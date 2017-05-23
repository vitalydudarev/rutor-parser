# -*- coding: utf-8 -*-

from lxml import html, etree
from HTMLParser import HTMLParser


class PageParser:
    def __init__(self, page_str):
        self.__html_parser = HTMLParser()
        self.__tree = html.fromstring(page_str)
        self.__details_elem = None

    def is_valid(self):
        self.__details_elem = self.__tree.xpath('//table[@id="details"]')
        return len(self.__details_elem) > 0

    def parse(self):
        info = self.__get_info()

        category = info[u'Категория'].xpath('./a/text()')
        size = info[u'Размер'].xpath('text()')

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
