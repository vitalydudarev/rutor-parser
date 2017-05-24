from client import HttpClient
from page_parser import PageParser

client = HttpClient()
start_pos = 567951

for i in range(10):
    id = start_pos + i
    link = 'http://rutor.is/torrent/' + str(id)

    response = client.get_response(link)
    if not response.has_error:
        parser = PageParser(id, response.response_text)
        valid = parser.is_valid()
        if valid:
            torrent_info = parser.parse()
            print torrent_info.to_json()
        else:
            print str(id) + ' is invalid'
