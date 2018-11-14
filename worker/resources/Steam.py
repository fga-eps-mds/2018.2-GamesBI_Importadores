import os
import requests
import colorific
from PIL import Image

STEAM_OWNERS_MIN = int(os.environ['STEAM_OWNERS_MIN'])
STEAM_GAMES_LIMIT = int(os.environ['STEAM_GAMES_LIMIT'])


class Steam(object):

    def get_steam_data(self):
        url = 'http://steamspy.com/api.php?request=all'
        header = {'Accept': 'application/json'}
        request = requests.get(url, headers=header)
        status = request.status_code
        if status == 200:
            data = request.json()
            return self.filter_steam_games(data)
        else:
            return []

    def filter_steam_games(self, games_data):
        count = 0
        filtered_data = []
        for game in games_data.values():
            if self.valid_game(game):
                if count >= STEAM_GAMES_LIMIT:
                    break
                keys = ['appid', 'name', 'positive', 'negative', 'owners',
                        'average_forever', 'average_2weeks', 'price']

                filtered_data.append(
                    {key: game[key] if key in game else None for key in keys})

                additional_information = self.get_infos_game_steam(
                    filtered_data[count]['appid']
                )
                filtered_data[count].update(additional_information)
                count += 1
        return filtered_data

    def get_infos_game_steam(self, game_id):
        url = 'https://store.steampowered.com/api/appdetails?appids={}'.format(
            game_id)
        header = {'Accept': 'application/json'}
        request = requests.get(url, headers=header)
        status = request.status_code
        if status == 200:
            data = request.json()
            return self.filter_infos_game_steam(data)
        else:
            return {
                'r_average': None,
                'g_average': None,
                'b_average': None,
                'main_image': None,
                'languages': [],
                'genres': [],
                'screenshots': [],
                'release_date': None
            }

    def filter_infos_game_steam(self, game_data):
        for game in game_data.values():
            if 'data' in game:
                data = game["data"]
                keys = ['header_image', 'release_date']
                dict_simple_fields = {
                    key: data[key] if key in data else [] for key in keys
                }
                dict_simple_fields['release_date'] = self.get_release_date(
                    dict_simple_fields['release_date']
                )

                keys_array = ['supported_languages', 'genres', 'screenshots']
                dict_array_fields = {
                    key: data[key] if key in data else [] for key in keys_array
                }
                dict_array_fields['supported_languages'] = self.get_languages(
                    dict_array_fields['supported_languages']
                )
                dict_array_fields['genres'] = self.get_genres(
                    dict_array_fields['genres']
                )
                dict_array_fields['screenshots'] = self.get_screenshots(
                    dict_array_fields['screenshots']
                )

                pallete_game = self.get_pallete_game(
                    dict_array_fields['screenshots']
                )
                keys_pallets = ['r', 'g', 'b']
                dict_pallet_fields = {
                    key: pallete_game[key] if key in pallete_game else
                    None for key in keys_pallets
                }
                dict_result = {}
                dict_result.update(dict_simple_fields)
                dict_result.update(dict_array_fields)
                dict_result.update(dict_pallet_fields)
                return dict_result
        return {
            'r_average': None,
            'g_average': None,
            'b_average': None,
            'main_image': None,
            'supported_languages': [],
            'genres': [],
            'screenshots': [],
            'release_date': None
        }

    def get_release_date(self, dict_date):
        if 'date' in dict_date:
            return dict_date['date']
        else:
            return None

    def get_languages(self, str_languages):
        languages = []
        array_languages = str_languages.split(', ')
        for language in array_languages:
            strong = True if '<strong>' in language else False
            if strong:
                correct_format_language = language.split('<')[0]
                languages.append(correct_format_language)
            else:
                languages.append(language)
        return languages

    def get_genres(self, genres):
        array_genres = []
        for genre in genres:
            if 'description' in genre:
                array_genres.append(genre['description'])
        return array_genres

    def get_screenshots(self, screenshots):
        list_screenshots = []
        for screenshot in screenshots:
            if 'path_thumbnail' in screenshot:
                url = screenshot['path_thumbnail']
                pallete = self.get_palette(url)
                dictionary_screenshot = {
                    'url': url,
                    'palette': pallete
                }
            else:
                dictionary_screenshot = None
            list_screenshots.append(dictionary_screenshot)
        return list_screenshots

    def get_pallete_game(self, screenshots):
        palletes = []
        for screenshot in screenshots:
            palletes.append(screenshot['palette'])
        return self.get_average_pallets(palletes)

    def valid_game(self, game):
        if 'owners' in game:
            owners_str = game['owners']
            owners = self.read_owners(owners_str)
            if owners > STEAM_OWNERS_MIN:
                return True
            else:
                return False
        else:
            return False

    def read_owners(self, str_owners):
        vector_numbers = self.valid_owners(str_owners)
        average = self.calculates_avarege(vector_numbers)
        return average

    def valid_owners(self, str_owners):
        low_average = str_owners.split(" .. ")[0]
        high_average = str_owners.split(" .. ")[1]
        low_average_valid = ""
        for number in low_average:
            if number != ",":
                low_average_valid = low_average_valid + number

        high_average_valid = ""
        for number in high_average:
            if number != ",":
                high_average_valid = high_average_valid + number

        low_average_int = int(low_average_valid)
        high_average_int = int(high_average_valid)
        return [low_average_int, high_average_int]

    def calculates_avarege(self, numbers):
        sum = 0
        for number in numbers:
            sum = sum + number
        return sum / len(numbers)

    def get_palette(self, img_url):
        request = requests.get(img_url, stream=True)
        status = request.status_code
        if status == 200:
            img = Image.open(request.raw)
            palette = colorific.extract_colors(img)
            array_colors = []
            for color in palette.colors:
                hex_value = colorific.rgb_to_hex(color.value)
                dictionary_colors = {
                    'r': color.value[0],
                    'g': color.value[1],
                    'b': color.value[2],
                    'hex': hex_value
                }
                array_colors.append(dictionary_colors)
            if palette.bgcolor is not None:
                hex_value = colorific.rgb_to_hex(palette.bgcolor.value)
                dictionary_colors = {
                    'r': palette.bgcolor.value[0],
                    'g': palette.bgcolor.value[1],
                    'b': palette.bgcolor.value[2],
                    'hex': hex_value
                }
                array_colors.append(dictionary_colors)
        else:
            array_colors = []
        return array_colors

    def get_average_pallets(self, array_photos):
        rgb_average = {
            'r': 0,
            'g': 0,
            'b': 0
        }
        qtd_pallets = 0
        for photo in array_photos:
            for palette in photo:
                rgb_average['r'] = rgb_average['r'] + palette['r']
                rgb_average['g'] = rgb_average['g'] + palette['g']
                rgb_average['b'] = rgb_average['b'] + palette['b']
                qtd_pallets += 1
        if qtd_pallets > 0:
            rgb_average['r'] = int(rgb_average['r'] / qtd_pallets)
            rgb_average['g'] = int(rgb_average['g'] / qtd_pallets)
            rgb_average['b'] = int(rgb_average['b'] / qtd_pallets)
            return rgb_average
        else:
            return []
