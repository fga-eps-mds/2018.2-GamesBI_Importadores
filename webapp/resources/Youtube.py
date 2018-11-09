import requests
import os

YOUTUBE_VIDEOS_LIMIT = int(os.environ['YOUTUBE_VIDEOS_LIMIT'])


class Youtube(object):

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
            print("-------------------------------------------------")
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
        status = request.status_code
        if status == 200:
            data = request.json()
            return self.filter_ids_youtube_game(data)
        else:
            data = {}
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
        status = request.status_code
        if status == 200:
            data = request.json()
            return self.filter_video_youtube_gama(data)
        else:
            data = {}
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
