from flask_restful import Resource
# from flask import jsonify
import requests
import operator
import os
from functools import reduce
# from pprint import pprint
from urllib.parse import quote

import colorific
from PIL import Image

TWITCH_HEADER = {'Client-ID': 'nhnlqt9mgdmkf9ls184tt1nd753472', 'Accept': 'application/json'}
YOUTUBE_VIDEOS_LIMIT = int(os.environ['YOUTUBE_VIDEOS_LIMIT'])
STEAM_OWNERS_MIN = int(os.environ['STEAM_OWNERS_MIN'])
STEAM_GAMES_LIMIT = int(os.environ['STEAM_GAMES_LIMIT'])

class Steam(Resource):

    def get(self):
        # Declaracao do array de objetos que será enviado para o crossData
        array_post = []
        # Busca os jogos da steam e retorna um array de jogos selecionados
        array_steam_data = self.get_steam_data()
        for game_steam in array_steam_data:
            game_youtube = self.get_youtube_data(game_steam['name'])
            game_twitch =  self.get_twitch_data(game_steam['name'])
            dictionary_game = self.merge_data(game_steam, game_youtube, game_twitch)
            array_post.append(dictionary_game)

        # req = requests.post("http://web:8000/import_data/api/", json=array_post)
        # return req.json()
        return array_post

# >>>>>>>>>>>>>>>>>> STEAM SECTION <<<<<<<<<<<<<<<<<<<<<<

    def get_screens_game(self):
        url = 'https://store.steampowered.com/api/appdetails?appids=10'
        header = {'Accept': 'application/json'}
        request = requests.get(url, headers=header)
        data = request.json()
        #print(data)
        self.filter_screens_game(data)


# Requisita todos os jogos da steam e retorna um array com jogos selecionados
    def get_steam_data(self):
        url = 'http://steamspy.com/api.php?request=all'
        header = {'Accept': 'application/json'}
        request = requests.get(url, headers=header)
        data = request.json()
        return self.filter_steam_games(data)

    # Filtra os dados da steam e retorna um array com jogos selecionados
    def filter_steam_games(self, games_data):
        select_games = []
        count = 0

        for game in games_data.values():
            if self.valid_game(game):
                if count >= STEAM_GAMES_LIMIT:
                    break

                count += 1
                additional_information = {
                    'genre': None,
                    'languages': None
                }
                if 'appid' in game:
                    id = game['appid']
                    additional_information = self.get_infos_game_steam(id)
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
                filtered_data = {
                    'id': id,
                    'name': name,
                    'positive_reviews_steam': positive,
                    'negative_reviews_steam': negative,
                    'owners': owners,
                    'average_forever': average_forever,
                    'average_2weeks': average_2weeks,
                    'price': price,
                    'languages': additional_information['languages'],
                    'genre': additional_information['genre']
                }
                select_games.append(filtered_data)

        # Pegando somente 10 por vez para os testes
        return select_games

    # Requisita jogo individualmente e retorna um dicionario com languages e genre referentes a um jogo
    def get_infos_game_steam(self, id_game):
        url = 'http://steamspy.com/api.php?request=appdetails&appid={}'.format(id_game)
        header = {'Accept': 'application/json'}
        request = requests.get(url, headers=header)
        data = request.json()
        return self.filter_infos_game_steam(data)

    # Filtra dados de um jogo e retorna um dicionario com languages e genre
    def filter_infos_game_steam(self, game_data):
        if 'languages' in game_data:
            languages = game_data['languages'].split(',')[0]
        else:
            languages = None

        if 'genre' in game_data:
            genre = game_data['genre'].split(", ")[0]
        else:
            genre = None
        return {
            'genre': genre,
            'languages': languages
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

    # Recebe uma string de owners, as separa em dois inteiros e retorna a media entra elas
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


# >>>>>>>>>>>>>>>>>> YOUTUBE SECTION <<<<<<<<<<<<<<<<<<<<<<


    def get_youtube_data(self, game_name):
        # Busca o array de ids de videos no youtube relacionados a cada jogo
        array_ids_youtube_game = self.get_ids_youtube_game(game_name)
        dictionary_game = {
            # 'id':qtd_jogos,
            'name': game_name,
            'count_videos': len(array_ids_youtube_game),
            'count_views': 0,
            'count_likes': 0,
            'count_dislikes': 0,
            'count_favorites': 0,
            'count_comments': 0
        }
        # Percorre array de ids de videos do youtube
        for id in array_ids_youtube_game:
            video_data = self.get_video_youtube_data(id)
            print("Requisitando video com ID: {}".format(id))
            print("------------------------------------------")
            dictionary_game['count_views'] = dictionary_game['count_views'] + video_data['count_views']
            dictionary_game['count_likes'] = dictionary_game['count_likes'] + video_data['count_likes']
            dictionary_game['count_dislikes'] = dictionary_game['count_dislikes'] + video_data['count_dislikes']
            dictionary_game['count_favorites'] = dictionary_game['count_favorites'] + video_data['count_favorites']
            dictionary_game['count_comments'] = dictionary_game['count_comments'] + video_data['count_comments']

        return dictionary_game


    # Requisita um jogo no youtube e retorna um array com todos os ID's de videos relacionados
    def get_ids_youtube_game(self, game_name):
        header={'Accept':'application/json'}
        key='AIzaSyDmDXP_gaB7cog4f0slbbdJ3RACsY5WQIw'
        url= 'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults={}&q={}GAMEPLAY&key={}'.format(
            YOUTUBE_VIDEOS_LIMIT,
            game_name,
            key,
        )
        request = requests.get(url, headers=header)
        data = request.json()
        return self.filter_ids_youtube_game(data)

    # Retorna um array com todos os ID's de videos relacionados a um jogo
    def filter_ids_youtube_game(self, youtube_results):
        items=[]
        if 'items' in youtube_results:
            items=youtube_results['items']

        list_id=[]
        for item in items:
            if 'id' in item:
                if 'videoId' in item['id']:
                    id=item['id']['videoId']
                    list_id.append(id)
                else:
                    id= None
            else:
                id=None
        return list_id

    # Requisita as informações de um video do youtube e retorna um objeto com essas informações
    def get_video_youtube_data(self, id_video):
        header = {'Accept': 'application/json'}
        key = 'AIzaSyDmDXP_gaB7cog4f0slbbdJ3RACsY5WQIw'
        url = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={}&key={}'.format(id_video, key)
        request = requests.get(url, headers=header)
        data = request.json()
        return self.filter_video_youtube_gama(data)

    # Filtra os dados de um video do youtube e retorna um objeto com esses dados
    def filter_video_youtube_gama(self, video_data):
        count_views = 0
        count_likes = 0
        count_dislikes = 0
        count_favorites = 0
        count_comments = 0
        if 'items' in video_data:
            items=video_data['items']
            for item in items:
                if 'statistics' in item:
                    if 'viewCount' in item['statistics']:
                        count_views = item['statistics']['viewCount']

                    if 'likeCount' in item['statistics']:
                        count_likes = item['statistics']['likeCount']

                    if 'dislikeCount' in item['statistics']:
                        count_dislikes = item['statistics']['dislikeCount']

                    if 'favoriteCount' in item['statistics']:
                        count_favorites = item['statistics']['favoriteCount']

                    if 'commentCount' in item['statistics']:
                        count_comments = item['statistics']['commentCount']

        filtered_data_video = {
            'count_views': int(count_views),
            'count_likes': int(count_likes),
            'count_dislikes': int(count_dislikes),
            'count_favorites': int(count_favorites),
            'count_comments': int(count_comments)
        }
        return filtered_data_video

# >>>>>>>>>>>>>>>>>> TWICH SECTION <<<<<<<<<<<<<<<<<<<<<<

    def get_twitch_data(self, game_name):
        url = 'https://api.twitch.tv/helix/games?name={}'.format(quote(game_name))

        game_data = requests.get(url, headers=TWITCH_HEADER)
        print(game_name)

        ndata = game_data.json()
        print(ndata)

        return self.filter_game_data(ndata['data'][0])

    def filter_game_data(self, ndata):
        total_views = 0

        game_id = 0;
        if 'id' in ndata:
            game_id = ndata['id']

        streams = self.get_streams(game_id)

        total_views = 0
        if len(streams) != 0:
            total_views = reduce(operator.add, [x['viewer_count'] if x['viewer_count'] != None else 0 for x in streams])

        print("Total views {}".format(total_views))

        return {
            'total_views': total_views,
            'streams': streams
        }


    def get_streams(self, game_id):
        url =  'https://api.twitch.tv/helix/streams?game_id={}'.format(game_id)

        stream_data = requests.get(url, headers=TWITCH_HEADER)
        ndata = stream_data.json()

        return self.filter_stream_data(ndata)

    def filter_stream_data(self, ndata):
        filtered_data = []

        for data in ndata['data']:
            keys = ['language', 'game_id', 'started_at', 'type', 'viewer_count']
            filtered_data.append({ key: data[key] if key in data else None for key in keys })

        return filtered_data[:2]

# >>>>>>>>>>>>>>>>>> PALLETE SECTION <<<<<<<<<<<<<<<<<<<<<<

    # Recebe uma url de uma imagem e retorna um array de dicionarios, onde cada
    # dicionario representa uma cor da paleta de cores da imagem
    def get_palette(self, img_url):
        img = Image.open(requests.get(img_url, stream=True).raw)
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

        return array_colors

    # Recebe um array de arrays retornardos pela funcao get_pallete e retorna um
    # dicionario com a média de cores do jogo
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
                qtd_pallets+=1

        rgb_average['r'] = int(rgb_average['r'] / qtd_pallets)
        rgb_average['g'] = int(rgb_average['g'] / qtd_pallets)
        rgb_average['b'] = int(rgb_average['b'] / qtd_pallets)

        return rgb_average


# >>>>>>>>>>>>>>>>>> MERGE SECTION <<<<<<<<<<<<<<<<<<<<<<

    def merge_data(self, steam_game, youtube_game, twitch_game):
        return {
            # Dados Steam
            'name': steam_game['name'],
            'positive_reviews_steam': steam_game['positive_reviews_steam'],
            'negative_reviews_steam': steam_game['negative_reviews_steam'],
            'owners': steam_game['owners'],
            'average_forever': steam_game['average_forever'],
            'average_2weeks': steam_game['average_2weeks'],
            'price': steam_game['price'],
            'languages': steam_game['languages'],
            'genre': steam_game['genre'],
            # Dados Youtube
            'count_videos': youtube_game['count_videos'],
            'count_views': youtube_game['count_views'],
            'count_likes': youtube_game['count_likes'],
            'count_dislikes': youtube_game['count_dislikes'],
            'count_comments': youtube_game['count_comments'],
            # Dados Twitch
            'total_views': twitch_game['total_views'],
            'streams': twitch_game['streams']
        }
