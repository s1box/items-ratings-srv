"""
(c) 2023 Mykola Morhun
Demo Python Flask REST API server with MySQL database.

This program is free software: you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation,
either version 2 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.
"""

import os

from flask import Flask
from flask_cors import CORS

from items_client import ItemsClient
from db_client import RatingMysqlClient

from status_api import StatusApi
from rating_api import RatingApi

RATING_TABLE_NAME = "items_rating"

def configure_app(app: Flask, db_client: RatingMysqlClient, items_client: ItemsClient):
    status_api = StatusApi(db_client, items_client)
    rating_api = RatingApi(db_client, items_client)

    @app.route('/')
    def default_endpoint():
        return '<p>Navigate to /status to check API status</p>'

    @app.route('/status')
    def status():
        return status_api.status()

    @app.route('/items/<int:item_id>/rating',methods=['POST'])
    def post_rating(item_id):
        return rating_api.post_rating(item_id)

    @app.route('/items/<int:item_id>/ratings')
    def get_all_ratings(item_id):
        return rating_api.get_all_ratings(item_id)

    @app.route('/items/<int:item_id>/rating')
    def get_average_rating(item_id):
        return rating_api.get_average_rating(item_id)

    @app.route('/items/random/rating')
    def get_random_item_and_rating():
        return rating_api.get_random_item_and_rating()


if __name__ == "__main__":
    _host = os.getenv('HOSTNAME')
    if _host is None:
        _host = '127.0.0.1'
    _port = os.getenv('PORT')
    if _port is None:
        _port = 8080

    _items_service_host = os.getenv('ITEMS_SERVICE_HOSTNAME')
    _items_service_port = os.getenv('ITEMS_SERVICE_PORT')

    app = Flask(__name__)
    CORS(app)
    db_client = RatingMysqlClient(RATING_TABLE_NAME, app)
    items_client = ItemsClient(_items_service_host, _items_service_port)

    configure_app(app, db_client, items_client)

    app.run(host=_host, port=_port)
