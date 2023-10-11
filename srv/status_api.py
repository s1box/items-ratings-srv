from flask import jsonify

from db_client import RatingMysqlClient
from items_client import ItemsClient

class StatusApi:

    def __init__(self, db_client: RatingMysqlClient, items_client: ItemsClient):
        self.__db_client = db_client
        self.__items_client = items_client


    def status(self):
        databaseResp = self.__db_client.ping()
        itemsServiceResp = self.__items_client.status()

        resp_json = {
            'database': databaseResp,
            'items_service': itemsServiceResp,
        }
        resp = jsonify(resp_json)
        resp.status_code = 200
        return resp

