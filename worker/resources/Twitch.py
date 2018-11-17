import requests
from functools import reduce
import operator
from urllib.parse import quote
import time

TWITCH_HEADER = {'Client-ID': 'nhnlqt9mgdmkf9ls184tt1nd753472', 'Accept': 'application/json'}


class Twitch(object):

    def get_twitch_data(self, game_name):
        url = 'https://api.twitch.tv/helix/games?name={}'.format(quote(game_name))
        time.sleep(3)
        game_data = requests.get(url, headers=TWITCH_HEADER)
        status = game_data.status_code
        if status == 200:
            ndata = game_data.json()
            return self.filter_game_data(ndata)
        else:
            return {
                'total_views': None,
                'streams': []
            }

    def filter_game_data(self, ndata):
        total_views = 0
        streams = []
        if 'data' in ndata:
            data = ndata['data']
            game_id = None
            for info in data:
                if 'id' in info:
                    game_id = info['id']
            streams = self.get_streams(game_id)

        total_views = 0
        if len(streams) != 0:
            total_views = reduce(operator.add, [x['viewer_count'] if x['viewer_count'] != None else 0 for x in streams])
            return {
                'total_views': total_views,
                'streams': streams
            }
        else:
            return {
                'total_views': None,
                'streams': []
            }

    def get_streams(self, game_id):
        url = 'https://api.twitch.tv/helix/streams?game_id={}'.format(game_id)
        time.sleep(3)
        stream_data = requests.get(url, headers=TWITCH_HEADER)
        status = stream_data.status_code
        if status == 200:
            ndata = stream_data.json()
            return self.filter_stream_data(ndata)
        else:
            return []

    def filter_stream_data(self, ndata):
        filtered_data = []
        for data in ndata['data']:
            keys = ['language', 'game_id', 'started_at', 'type', 'viewer_count']
            filtered_data.append({ key: data[key] if key in data else None for key in keys })

        return filtered_data[:2]
