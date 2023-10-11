import unittest

from flask import Flask

from main import configure_app


class FakeItemsClient:
    def status(self):
        return "OK"

    def get_item(self, item_id):
        if item_id == 1:
            return {'id': '1', 'name': 'id1'}
        return {'message': 'not found'}


class FakeDbClient:
    def ping(self):
        return "OK"

    def add_rating(self, item_id, item_rating):
        pass

    def get_ratings_for_item(self, item_id):
        if item_id == 1:
            return [4, 5, 1, 4]
        return []

    def get_average_rating_for_item(self, item_id):
        if item_id == 1:
            return 3.5
        return None

    def get_random_rating_record(self):
        return (1, 4)



class RatingApiTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.app = Flask(__name__)
        configure_app(self.app, FakeDbClient(), FakeItemsClient())
        self.app.config['TESTING'] = True
        self.app_test_client = self.app.test_client()


    def test_ping(self):
        response = self.app_test_client.get('/status')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['database'], 'OK')
        self.assertEqual(data['items_service'], 'OK')


    def test_get_all_ratings_existing_item(self):
        response = self.app_test_client.get('/items/1/ratings')
        data = response.get_json()

        self.assertEqual(response.status_code, 200, 'wrong status code')
        self.assertEqual(data['item_id'], 1, 'wrong item id')
        self.assertEqual(data['item_name'], 'id1', 'wrong item name')
        self.assertCountEqual(data['ratings'], [4, 5, 1, 4], 'wrong rating data')


    def test_get_all_ratings_non_existing_item(self):
        response = self.app_test_client.get('/items/2/ratings')
        data = response.get_json()

        self.assertEqual(response.status_code, 400, 'wrong status code')
        self.assertNotEqual(data['message'], '')


    def test_get_average_rating_existing_item(self):
        response = self.app_test_client.get('/items/1/rating')
        data = response.get_json()

        self.assertEqual(response.status_code, 200, 'wrong status code')
        self.assertEqual(data['item_id'], 1, 'wrong item id')
        self.assertEqual(data['item_name'], 'id1', 'wrong item name')
        self.assertEqual(data['avg_rating'], 3.5, 'wrong rating data')


    def test_get_average_rating_non_existing_item(self):
        response = self.app_test_client.get('/items/2/rating')
        data = response.get_json()

        self.assertEqual(response.status_code, 400, 'wrong status code')
        self.assertNotEqual(data['message'], '')


    def test_post_rating_number_type(self):
        response = self.app_test_client.post('/items/1/rating', json={'rating': 4})

        self.assertEqual(response.status_code, 201, 'wrong status code')


    # def test_post_rating_string_type(self):
    #     response = self.app_test_client.post('/items/1/rating', json={'rating': '4'})

    #     self.assertEqual(response.status_code, 201, 'wrong status code')


    def test_post_rating_invalid_rating_sent(self):
        response = self.app_test_client.post('/items/1/rating', json={'rating': 10})
        data = response.get_json()

        self.assertEqual(response.status_code, 400, 'wrong status code')
        self.assertNotEqual(data['message'], '')


    def test_post_rating_no_rating_sent(self):
        response = self.app_test_client.post('/items/2/rating')
        data = response.get_json()

        self.assertEqual(response.status_code, 400, 'wrong status code')
        self.assertNotEqual(data['message'], '')


    def test_post_rating_non_existing_item(self):
        response = self.app_test_client.post('/items/2/rating', json={'rating': 4})
        data = response.get_json()

        self.assertEqual(response.status_code, 400, 'wrong status code')
        self.assertNotEqual(data['message'], '')



if __name__ == '__main__':
    unittest.main()
