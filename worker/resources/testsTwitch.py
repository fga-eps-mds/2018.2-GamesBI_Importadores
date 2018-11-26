import unittest
import requests_mock
from . import Twitch

class TestImporter(unittest.TestCase):

    #Twitch
    def test_get_twitch_data_bad_request(self):
        self.twitch = Twitch.Twitch()

        game_name = 'asdazsd'
        data = {
        'total_views': None,
        'streams': []
        }

        response = self.twitch.get_twitch_data(game_name)
        self.assertEqual(response, data)

    def test_get_streams(self):
        self.twitch = Twitch.Twitch()
        game_id = 'asdazsd'

        response = self.twitch.get_streams(game_id)
        self.assertEqual(len(response), 0)

if __name__ == '__main__':
    unittest.main()
