# -*- coding: utf-8 -*-

from client import HttpClient
from page_parser import PageParser
import time
import json
import os.path
from json import JSONEncoder


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

def get_torrent_id():
    if os.path.exists('hist.txt'):
        with open('hist.txt', 'r') as file:
            return int(file.read())
    else:
        return 568847

def save_history(torrent_id):
    with open('hist.txt', 'w') as file:
        file.write(str(torrent_id))

def save_dump(contents):
    with open('dump.txt', 'w') as file:
        file.write(contents.encode('utf-8'))

def get_dump():
    if os.path.exists('dump.txt'):
        with open('dump.txt', 'r') as file:
            return json.loads(file.read())
    else:
        return []

def dump():
    client = HttpClient()
    torrent_id = get_torrent_id()

    last_torrent_id = torrent_id

    res = get_dump()

    for i in range(150):
        id = torrent_id - i
        last_torrent_id = id
        link = 'http://rutor.is/torrent/' + str(id)

        response = client.get_response(link)
        if not response.has_error:
            parser = PageParser(id, response.response_text)
            valid = parser.is_valid()
            if valid:
                torrent_info = parser.parse()
                if torrent_info.category == u'Зарубежные фильмы' or torrent_info.category == u'Наши фильмы':
                    res.append(torrent_info)
            else:
                print str(id) + ' is invalid'

        time.sleep(5)

    dump = json.dumps(res, cls=MyEncoder, ensure_ascii=False)
    save_dump(dump)
    save_history(last_torrent_id + 1)
    print 'finished'

dump()
