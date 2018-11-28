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

    @requests_mock.Mocker()
    def test_get_twitch_data(self, request_mock):
        self.twitch = Twitch.Twitch()
        game_name = 'PUBG'
        url = 'https://api.twitch.tv/helix/games?name={}'.format(game_name)
        data_url = {
            "data": [
                {
                    "id": "493057",
                    "name": "PLAYERUNKNOWN'S BATTLEGROUNDS",
                    "box_art_url": "https://static-cdn.jtvnw.net/ttv-boxart/PLAYERUNKNOWN%27S%20BATTLEGROUNDS-{width}x{height}.jpg"
                }
            ]
        }

        request_mock.get(url, json=data_url)

        game_id = '493057'
        url_id = 'https://api.twitch.tv/helix/streams?game_id={}'.format(game_id)

        data_id = {
            "data": [
                {
                    "id": "31432712304",
                    "user_id": "22159551",
                    "user_name": "Lumi",
                    "game_id": "493057",
                    "community_ids": [
                        "01d41280-9332-4f54-b77a-a20f577beade",
                        "434e0896-4c27-4c87-9275-cbfba2b323f5",
                        "b0e7cf13-4131-4f1b-9810-d88087de024b"
                    ],
                    "type": "live",
                    "title": ":)",
                    "viewer_count": 1032,
                    "started_at": "2018-11-27T21:53:46Z",
                    "language": "en",
                    "thumbnail_url": "https://static-cdn.jtvnw.net/previews-ttv/live_user_lumi-{width}x{height}.jpg",
                    "tag_ids": [
                        "6ea6bca4-4712-4ab9-a906-e3336a9d8039",
                        "ab340187-1794-4630-9eab-e3b75cc86381"
                    ]
                },
                {
                    "id": "31426144768",
                    "user_id": "121652526",
                    "user_name": "LittleBigWhale",
                    "game_id": "493057",
                    "community_ids": [
                        "229f348c-3bdc-45af-8e66-3e7562f7c2a5"
                    ],
                    "type": "live",
                    "title": "Duo ft. Gius",
                    "viewer_count": 602,
                    "started_at": "2018-11-27T14:06:34Z",
                    "language": "fr",
                    "thumbnail_url": "https://static-cdn.jtvnw.net/previews-ttv/live_user_littlebigwhale-{width}x{height}.jpg",
                    "tag_ids": [
                        "6f655045-9989-4ef7-8f85-1edcec42d648"
                    ]
                }
            ]
        }
        request_mock.get(url_id, json=data_id)

        data = {
            'total_views': 1634,
            'streams': [
                {
                    'game_id': '493057',
                    'language': 'en',
                    'started_at': '2018-11-27T21:53:46Z',
                    'type': 'live',
                    'viewer_count': 1032
                },
                {
                    'game_id': '493057',
                    'language': 'fr',
                    'started_at': '2018-11-27T14:06:34Z',
                    'type': 'live',
                    'viewer_count': 602
                }
            ]
        }

        response = self.twitch.get_twitch_data(game_name)

        self.assertEqual(response, data)


if __name__ == '__main__':
    unittest.main()
