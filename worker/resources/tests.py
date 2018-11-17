from Youtube import Youtube
from Twitch import Twitch
from Steam import Steam
from Importer import Importer
import unittest
import requests_mock


class TestImporter(unittest.TestCase):

	def setUp(self):
		self.data_name = "Counter Strike"
		self.steam = Steam()
		self.youtube = Youtube()
		self.twitch = Twitch()
		self.importer = Importer()

	def test_status_code_Steam(self):
		response = self.steam.get_steam_data()
		self.assertNotEqual(len(response), 0)

	def test_get_importadores(self):
		response = self.import.get(self)
		self.assertNotEqual(len(response), 0)


	@requests_mock.Mocker()
	def test_requisicao_mock_steam(self, request_mock):
        url = 'http://steamspy.com/api.php?request=all'

        data = [
            {
                "id_steam": 123,
                "name": "Test 1",
                "positive_reviews_steam": 1923123,
                "negative_reviews_steam": 12121,
                "owners": 130000,
                "average_forever": 2127,
                "average_2weeks": 132,
                "price": "0",
                "languages": [
                    "mandarim", "espanhol"
                ],
                "genres": [
                    "tiro", "porrada"
                ],
                "main_image": "google.com",
                "screenshots": [
                    {
                        "url": "https://steamcdn-a.akamaihd.net/steam/apps/570/ss_86d675fdc73ba10462abb8f5ece7791c5047072c.600x338.jpg?t=1536248487",
                        "palette": [
                            {
                                "r": 8,
                                "g": 16,
                                "b": 2,
                                "hex": "#1aa741"
                            },
                            {
                                "r": 34,
                                "g": 12,
                                "b": 37,
                                "hex": "#2e204d"
                            },
                            {
                                "r": 22,
                                "g": 48,
                                "b": 34,
                                "hex": "#484454"
                            },
                            {
                                "r": 121,
                                "g": 80,
                                "b": 254,
                                "hex": "#b5b49a"
                            },
                            {
                                "r": 19,
                                "g": 26,
                                "b": 21,
                                "hex": "#3b4233"
                            }
                        ]
                    },
                ],
                "release_date": "1 Feb, 1999",
                "r_average": 83,
                "g_average": 82,
                "b_average": 74,
            },
        ]
		request_mock.get(url, json=data)

		self.assertEqual(self.steam.get_steam_data(), data)


if __name__ == '__main__':
    unittest.main()
