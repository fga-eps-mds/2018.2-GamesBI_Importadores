from . import Youtube, Twitch, Steam
# import requests


class Importer():

    def get(self):
        array_post = []
        steam = Steam.Steam()
        youtube = Youtube.Youtube()
        twitch = Twitch.Twitch()
        print("Inicio de importação dos jogos da steam ...\n")
        array_steam_data = steam.get_steam_data()
        for game_steam in array_steam_data:
            print("Jogo: {}".format(game_steam['name']))
            print("Importando dados do youtube ...")
            game_youtube = youtube.get_youtube_data(game_steam['name'])
            print("Importando dados da twitch ...")
            game_twitch = twitch.get_twitch_data(game_steam['name'])
            dictionary_game = self.merge_data(
                game_steam, game_youtube, game_twitch)
            array_post.append(dictionary_game)


            print("Jogo {} importado com sucesso!\n".format(game_steam['name']))


        # requests.post("http://web:8000/api/", json=array_post)
        return array_post

    def merge_data(self, steam_game, youtube_game, twitch_game):
        merge_dictionary = {
            # Steam data
            'id_steam': steam_game['appid'],
            'name': steam_game['name'],
            'positive_reviews_steam': steam_game['positive'],
            'negative_reviews_steam': steam_game['negative'],
            'owners': steam_game['owners'],
            'average_forever': steam_game['average_forever'],
            'average_2weeks': steam_game['average_2weeks'],
            'price': steam_game['price'],
            'languages': steam_game['supported_languages'],
            'genres': steam_game['genres'],
            'main_image': steam_game['header_image'],
            'screenshots': steam_game['screenshots'],
            'release_date': steam_game['release_date'],
            'r_average': steam_game['r'],
            'g_average': steam_game['g'],
            'b_average': steam_game['b'],
            # Youtube data
            'count_videos': youtube_game['count_videos'],
            'count_views': youtube_game['count_views'],
            'count_likes': youtube_game['count_likes'],
            'count_dislikes': youtube_game['count_dislikes'],
            'count_comments': youtube_game['count_comments'],
            # Twitch data
            'total_views': twitch_game['total_views'],
            'streams': twitch_game['streams']
        }
        return merge_dictionary
