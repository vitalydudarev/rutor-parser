from client import HttpClient
from page_parser import PageParser

client = HttpClient()
start_pos = 567951

for i in range(1):
    id = start_pos + i
    link = 'http://rutor.is/torrent/' + str(id)

    response = client.get_response(link)
    if not response.has_error:
        parser = PageParser(response.response_text)
        valid = parser.is_valid()
        if valid:
            parser.parse()
