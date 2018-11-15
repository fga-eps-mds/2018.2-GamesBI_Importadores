from rest_framework.test import APITestCase
from . import You-tube, Twitch, Steam
from rest_framework import status


class ImporterTest(APITestCase):

	def setUp(self):

		#self.url = reverse("Steam")

        self.data = = {
            'id': 123,
            'name': teste,
            'positive_reviews_steam': 10,
            'negative_reviews_steam': 5,
            'owners': 100000,
            'average_forever': 500,
            'average_2weeks': 20,
            'price': 50
        }

	def tearDown(self):

    def test_status_code_Steam(self):

        response = self.client.get_steam_data(self)
        self.assertEqual(response.status_code, status.HTTP_200)

	def test_status_code_BAD_REQUEST_Steam(self):

		response = self.client.get_steam_data(self)
		self.assertNotEqual(response.status_code, status.HTTP_200)
