import os
import requests
import colorific
from PIL import Image

STEAM_OWNERS_MIN = int(os.environ['STEAM_OWNERS_MIN'])
STEAM_GAMES_LIMIT = int(os.environ['STEAM_GAMES_LIMIT'])


class Steam(object):

    # Requisita todos os jogos da steam e retorna
    # um array com jogos selecionado
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

    # Filtra os dados da steam e retorna um array com jogos selecionados
    def filter_steam_games(self, games_data):
        select_games = []
        count = 0
        for game in games_data.values():
            if self.valid_game(game):
                if count >= STEAM_GAMES_LIMIT:
                    break
                count += 1
                if 'appid' in game:
                    id = game['appid']
                else:
                    id = None
                if 'name' in game:
                    name = game['name']
                else:
                    name = None
                if 'positive' in game:
                    positive = game['positive']
                else:
                    positive = None
                if 'negative' in game:
                    negative = game['negative']
                else:
                    negative = None
                if 'owners' in game:
                    owners_str = game['owners']
                    owners = self.read_owners(owners_str)
                else:
                    owners_str = None
                if 'average_forever' in game:
                    average_forever = game['average_forever']
                else:
                    average_forever = None
                if 'average_2weeks' in game:
                    average_2weeks = game['average_2weeks']
                else:
                    average_2weeks = None
                if 'price' in game:
                    price = game['price']
                else:
                    price = None
                additional_information = self.get_infos_game_steam(id)
                filtered_data = {
                    'id': id,
                    'name': name,
                    'positive_reviews_steam': positive,
                    'negative_reviews_steam': negative,
                    'owners': owners,
                    'average_forever': average_forever,
                    'average_2weeks': average_2weeks,
                    'price': price,
                    'main_image': additional_information['main_image'],
                    'languages': additional_information['languages'],
                    'genres': additional_information['genres'],
                    'release_date': additional_information['release_date'],
                    'screenshots': additional_information['screenshots'],
                    'r_average': additional_information['r_average'],
                    'g_average': additional_information['g_average'],
                    'b_average': additional_information['b_average']
                }
                select_games.append(filtered_data)

        return select_games

    def get_infos_game_steam(self, game_id):
        url = 'https://store.steampowered.com/api/appdetails?appids={}'.format(game_id)
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

                if 'header_image' in data:
                    main_image = data['header_image']
                else:
                    main_image = None

                if 'supported_languages' in data:
                    array_languages = data['supported_languages'].split(', ')
                    languages = []
                    for language in array_languages:
                        strong = True if '<strong>' in language else False
                        if strong:
                            languages.append(language.split('<')[0])
                        else:
                            languages.append(language)
                else:
                    languages = []

                if 'genres' in data:
                    genres = []
                    array_genres = data["genres"]
                    for genre in array_genres:
                        if 'description' in genre:
                            genres.append(genre['description'])
                else:
                    genres = []

                list_screenshots = []
                if 'screenshots' in data:
                    list_pallets = []
                    for screenshot in data['screenshots']:
                        if 'path_thumbnail' in screenshot:
                            url = screenshot['path_thumbnail']
                            pallete = self.get_palette(url)
                            list_pallets.append(pallete)
                            dictionary_screenshot = {
                                'url': url,
                                'palette': pallete
                            }
                        else:
                            dictionary_screenshot = None
                        list_screenshots.append(dictionary_screenshot)
                    pallete_game = self.get_average_pallets(list_pallets)
                else:
                    pallete_game = []

                if 'release_date' in data:
                    release = data['release_date']
                    if 'date' in release:
                        release_date = release['date']
                    else:
                        release_date = None
                else:
                    release_date = None

                if 'r' in pallete_game:
                    r_average = pallete_game['r']
                else:
                    r_average = None

                if 'g' in pallete_game:
                    g_average = pallete_game['g']
                else:
                    g_average = None

                if 'b' in pallete_game:
                    b_average = pallete_game['b']
                else:
                    b_average = None

            return {
                'r_average': r_average,
                'g_average': g_average,
                'b_average': b_average,
                'main_image': main_image,
                'languages': languages,
                'genres': genres,
                'screenshots': list_screenshots,
                'release_date': release_date
            }

    # Valida se aquele jogo tem uma quantidade mínima de owners
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

    # Recebe uma string de owners e retorna a média entra elas
    def read_owners(self, str_owners):
        vector_numbers = self.valid_owners(str_owners)
        average = self.calculates_avarege(vector_numbers)
        return average

    # Recebe uma string de owners, as separa em dois
    # inteiros e retorna a media entra elas
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

    # Recebe um array de numeros e retorna a media entre eles
    def calculates_avarege(self, numbers):
        sum = 0
        for number in numbers:
            sum = sum + number
        return sum / len(numbers)

    # Recebe uma url de uma imagem e retorna um array de dicionarios, onde cada
    # dicionario representa uma cor da paleta de cores da imagem
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

    # Recebe um array de arrays retornardos pela funcao get_pallete
    # e retorna um dicionario com a média de cores do jogo
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
