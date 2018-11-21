from Youtube import Youtube
from Twitch import Twitch
from Steam import Steam
from Importer import Importer
import unittest
import requests_mock


class TestImporter(unittest.TestCase):

	@requests_mock.Mocker()
	def setUp(self, request_mock):
		self.data_name = "Counter Strike"
		self.steam = Steam()
		self.youtube = Youtube()
		self.twitch = Twitch()
		self.importer = Importer()

		url_steam = 'http://steamspy.com/api.php?request=all'
		url_steam2 = 'https://store.steampowered.com/api/appdetails?appids=730'

		url_youtube = 'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=Counter-Strike&q=50GAMEPLAY&key=AIzaSyDmDXP_gaB7cog4f0slbbdJ3RACsY5WQIw'
		url_youtube2 = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id=15454&key=AIzaSyDmDXP_gaB7cog4f0slbbdJ3RACsY5WQIw\'

		data_steam = {
			"730":{
				"appid":730,
				"name":"Counter-Strike: Global Offensive",
				"developer":"Valve",
				"publisher":"Valve",
				"score_rank":72,
				"positive":2435010,
				"negative":314329,
				"userscore":88,
				"owners":"20,000,000 .. 50,000,000",
				"average_forever":33061,
				"average_2weeks":988,
				"median_forever":15008,
				"median_2weeks":405,
				"price":"1499",
				"initialprice":"1499",
				"discount":"0"
			}
						}

		data_steam2 = [
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

		data_youtube = 'item':[
								'id':[
										'videoId' : 15454
									]
							]
		data_youtube2 = 'items':[
			'statistics':{
	            'count_views': '123',
	            'count_likes': '1222',
	            'count_dislikes': '323',
	            'count_favorites': '3222',
	            'count_comments': '32333'
	        }
		]

		data_youtube3 = {
			'name': game_name,
			'count_videos': None,
			'count_views': None,
			'count_likes': None,
			'count_dislikes': None,
			'count_favorites': None,
			'count_comments': None
		}

		request_mock.get(url_steam, json=data_steam)
		request_mock.get(url_steam2, json=data_steam2)

		request_mock.get(url_youtube, json=data_youtube)
		request_mock.get(url_youtube2, json=data_youtube2)

	def test_status_code_Steam(self):
		response = self.steam.get_steam_data()
		self.assertNotEqual(len(response), 0)

	def test_get_importadores(self):
		response = self.import.get(self)
		self.assertNotEqual(len(response), 0)


	def test_requisicao_steam(self):

		self.assertEqual(self.steam.get_steam_data(), data_steam2)

	def test_requisicao_Yotube(self):

		self.assertEqual(self.youtube.get_youtube_data(), data_youtube3)

if __name__ == '__main__':
    unittest.main()
