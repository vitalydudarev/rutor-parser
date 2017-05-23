import urllib2
import urllib
import requests
from socket import timeout


class HttpClient:
    def __init__(self, proxy={}, timeout=None):
        self.__proxy = proxy
        self.__timeout = timeout

    def get_response(self, url):
        if len(self.__proxy) > 0:
            proxy = urllib2.ProxyHandler(self.__proxy)
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener)

        has_error = False
        response_text = ""

        try:
            if self.__timeout is None:
                u = urllib2.urlopen(url)
            else:
                u = urllib2.urlopen(url, timeout=self.__timeout)
            response_text = u.read()

        except (urllib2.HTTPError, urllib2.URLError):
            has_error = True
        except timeout:
            has_error = True
        except requests.exceptions.RequestException:
            has_error = True

        return Response(has_error, response_text)

    def post(self, url, headers, params):
        encoded_params = urllib.urlencode(params)

        return requests.post(url, data=encoded_params, headers=headers, proxies=self.__proxy)


class Response:
    def __init__(self, has_error, response_text):
        self.has_error = has_error
        self.response_text = response_text
