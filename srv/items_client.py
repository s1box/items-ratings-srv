import requests

from util import is_int

class ItemsClient:
    """ Client for Items microservice """

    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__protocol = "http://"

        port = ""
        if self.__port and is_int(self.__port):
            port = ":%s" % self.__port
        self.__baseUrl = "%s%s%s" % (self.__protocol, self.__host, port)


    def status(self):
        try:
            url = self.__baseUrl + "/status"
            response = requests.get(url)
            data = response.json()
            return data["database"]
        except Exception as e:
            print(e)
            return str(e)


    def get_item(self, item_id):
        try:
            url = "%s/items/%s" % (self.__baseUrl, item_id)
            response = requests.get(url)
            return response.json()
        except Exception as e:
            print(e)
            return {'error': str(e)}

