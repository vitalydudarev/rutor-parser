# -*- coding: utf-8 -*-

from client import HttpClient
from page_parser import PageParser
import time
import json
import os.path
from json import JSONEncoder
import threading
import pymysql.cursors


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

class Direction(object):
    UP = 1
    DOWN = 2

def save_to_db(result):
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             db='rutor_db',
                             charset='utf8mb4',
                             use_unicode=True,
                             cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `rutor` (`torrent_id`, `title`, `category`, `size`, `added`) VALUES (%s, %s, %s, %s, %s)"

            for item in result:
                cursor.execute(sql, (item.torrent_id, item.title, item.category, item.size, item.added))
        connection.commit()
    finally:
        connection.close()

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

run = True

def dump():
    client = HttpClient()
    torrent_id = get_torrent_id()
    res = get_dump()
    new_records = []

    last_torrent_id = torrent_id
    direction = Direction.UP

    if direction == Direction.UP:
        increment = 1
    else:
        increment = -1

    i = 0
    failed = 0

    while run:
        last_torrent_id = last_torrent_id + increment
        print str (last_torrent_id)
        link = 'http://rutor.is/torrent/' + str(last_torrent_id)

        response = client.get_response(link)
        if not response.has_error:
            parser = PageParser(last_torrent_id, response.response_text)
            valid = parser.is_valid()
            if valid:
                failed = 0
                torrent_info = parser.parse()
                if torrent_info.category == u'Зарубежные фильмы' or torrent_info.category == u'Наши фильмы':
                    res.append(torrent_info)
                    new_records.append(torrent_info)
            else:
                print str(last_torrent_id) + ' is invalid'
                failed = failed + 1
                if failed == 10:
                    print 'end of torrent list reached'
                    last_torrent_id = last_torrent_id - 10 - 1
                    break

        i = i + 1

        time.sleep(4)

    dump = json.dumps(res, cls=MyEncoder, ensure_ascii=False)
    save_dump(dump)
    save_history(last_torrent_id + increment)
    save_to_db(new_records)
    print 'finished'

thread = threading.Thread(target=dump)
thread.start()
'press any key and then Enter to exit'

while True:
    line = raw_input()
    run = False
    break
