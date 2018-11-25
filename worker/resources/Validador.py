import os
import requests

CROSSDATA_POST = (os.environ['CROSSDATA_POST'])

class Validador(object):

    def game_exists(self, game_name):
        url = '{}?name={}&partial'.format(CROSSDATA_POST, game_name)
        header = {'Accept': 'application/json'}
        request = requests.get(url, headers=header)
        status = request.status_code
        if status == 200:
            games = request.json()
            for game in games:
                if game['name'] == game_name:
                    return True
            return False
        else:
            return True
