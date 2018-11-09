from flask_restful import Resource
from . import Youtube, Twitch, Steam


class Importer(Resource):

    def get(self):
        array_post = []
        steam = Steam.Steam()
        youtube = Youtube.Youtube()
        twitch = Twitch.Twich()
        array_steam_data = steam.get_steam_data()
        for game_steam in array_steam_data:
            game_youtube = youtube.get_youtube_data(game_steam['name'])
            game_twitch =  twitch.get_twitch_data(game_steam['name'])
            dictionary_game = self.merge_data(game_steam, game_youtube, game_twitch)
            array_post.append(dictionary_game)

        return array_post

    def merge_data(self, steam_game, youtube_game, twitch_game):
        array = []
        # Dados Steam
        if (len(steam_game) == 0):
            return array
        else:
            steam_dictionary = {
                'id_steam': steam_game['id'],
                'name': steam_game['name'],
                'positive_reviews_steam': steam_game['positive_reviews_steam'],
                'negative_reviews_steam': steam_game['negative_reviews_steam'],
                'owners': steam_game['owners'],
                'average_forever': steam_game['average_forever'],
                'average_2weeks': steam_game['average_2weeks'],
                'price': steam_game['price'],
                'language': steam_game['language'],
                'genre': steam_game['genre'],
                'main_image': steam_game['main_image'],
                'screenshots': steam_game['screenshots'],
                'release_date': steam_game['release_date'],
                'r_average': steam_game['r_average'],
                'g_average': steam_game['g_average'],
                'b_average': steam_game['b_average']
            }

        # Dados Youtube
        if (len(youtube_game) == 0):
            youtube_dictionary = {
                'count_videos': None,
                'count_views': None,
                'count_likes': None,
                'count_dislikes': None,
                'count_comments': None
            }
        else:
            youtube_dictionary = {
                'count_videos': youtube_game['count_videos'],
                'count_views': youtube_game['count_views'],
                'count_likes': youtube_game['count_likes'],
                'count_dislikes': youtube_game['count_dislikes'],
                'count_comments': youtube_game['count_comments']
            }

        # Dados Twitch
        if (len(twitch_game) == 0):
            twitch_dictionary = {
                'total_views': None,
                'streams': None
            }
        else:
            twitch_dictionary = {
                'total_views': twitch_game['total_views'],
                'streams': twitch_game['streams']
            }

        merge_dictionary = {}
        merge_dictionary.update(steam_dictionary)
        merge_dictionary.update(youtube_dictionary)
        merge_dictionary.update(twitch_dictionary)
        return merge_dictionary
