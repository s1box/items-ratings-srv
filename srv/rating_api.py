import json

from flask import request, jsonify, Response

from db_client import RatingMysqlClient
from items_client import ItemsClient
from util import is_float

class RatingApi:

    def __init__(self, db_client: RatingMysqlClient, items_client: ItemsClient):
        self.__db_client = db_client
        self.__items_client = items_client


    def __bad_request(self, message):
        resp_json = { 'message': message }
        resp = jsonify(resp_json)
        resp.status_code = 400
        return resp

    def __internal_error(self, message):
        resp_json = {'message': message}
        resp = jsonify(resp_json)
        resp.status_code = 500
        return resp

    def post_rating(self, item_id):
        data = request.get_data()
        if not data:
            return self.__bad_request('rating is not set')
        json_data = json.loads(data)
        if not 'rating' in json_data:
            return self.__bad_request('rating is not set')

        rating = json_data['rating']
        if not is_float(rating) or (rating < 0 or rating > 5):
            return self.__bad_request('Invalid rating:' + str(rating))

        items_service_response = self.__items_client.get_item(item_id)
        if not 'id' in items_service_response:
            return self.__bad_request('Item with ID ' + str(item_id) + ' does not exist')

        self.__db_client.add_rating(item_id, rating)

        return Response(status = 201)


    def get_all_ratings(self, item_id):
        response = self.__items_client.get_item(item_id)
        if 'error' in response:
            return self.__internal_error(response['error'])
        if not 'id' in response:
            return self.__bad_request('Item with ID ' + str(item_id) + ' does not exist')

        ratings = self.__db_client.get_ratings_for_item(item_id)
        resp_json = {
            'item_id': item_id,
            'item_name': response['name'],
            'ratings': ratings,
        }
        resp = jsonify(resp_json)
        resp.status_code = 200
        return resp


    def get_average_rating(self, item_id):
        response = self.__items_client.get_item(item_id)
        if 'error' in response:
            return self.__internal_error(response['error'])
        if not 'id' in response:
            return self.__bad_request('Item with ID ' + str(item_id) + ' does not exist')

        avg_rating = self.__db_client.get_average_rating_for_item(item_id)
        resp_json = {
            'item_id': item_id,
            'item_name': response['name'],
            'avg_rating': avg_rating,
        }
        resp = jsonify(resp_json)
        resp.status_code = 200
        return resp


    def get_random_item_and_rating(self):
        record = self.__db_client.get_random_rating_record()
        resp_json = {
            'item_id': record[1],
            'rating': record[2],
        }
        resp = jsonify(resp_json)
        resp.status_code = 200
        return resp
