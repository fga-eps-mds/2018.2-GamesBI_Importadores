from flask_restful import Resource
# from flask import jsonify
import requests
# from pprint import pprint


class Steam(Resource):

    def get(self):
        # Declaracao do array de objetos que será enviado para o crossData
        arrayPOST = []
        # Busca os jogos da steam e retorna um array de jogos selecionados
        arraySteamData = self.getSteamData()
        for gameSteam in arraySteamData:
            gameYoutube = self.getYoutubeData(gameSteam['name'])
            # gameTwich = self.getTwitchData(gameSteam)
            # dictionaryGame = self.mergeData(gameSteam, gameYoutube, gameTwich)
            arrayPOST.append(dictionaryGame)

        # Ao final do for, criar requisição POST e enviar arrayPOST para o crossData

        return "OK"


# >>>>>>>>>>>>>>>>>> STEAM SECTION <<<<<<<<<<<<<<<<<<<<<<


    # Requisita todos os jogos da steam e retorna um array com jogos selecionados
    def getSteamData(self):
        url = 'http://steamspy.com/api.php?request=all'
        header = {'Accept': 'application/json'}
        request = requests.get(url, headers=header)
        data = request.json()
        return self.filterSteamGames(data)

    # Filtra os dados da steam e retorna um array com jogos selecionados
    def filterSteamGames(self, gamesData):
        selectGames = []
        for game in gamesData.values():
            if self.validGame(game):
                additionalInformation = {
                    'genre': None,
                    'languages': None
                }
                if 'appid' in game:
                    id = game['appid']
                    additionalInformation = self.getInfosGameSteam(id)
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
                    owners = self.readOwners(owners_str)
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
                    'languages': additionalInformation['languages'],
                    'genre': additionalInformation['genre']
                }
                selectGames.append(filtered_data)
        return selectGames

    # Requisita jogo individualmente e retorna um dicionario com languages e genre referentes a um jogo
    def getInfosGameSteam(self, idGame):
        url = 'http://steamspy.com/api.php?request=appdetails&appid={}'.format(idGame)
        header = {'Accept': 'application/json'}
        request = requests.get(url, headers=header)
        data = request.json()
        return self.filterInfosGameSteam(data)

    # Filtra dados de um jogo e retorna um dicionario com languages e genre
    def filterInfosGameSteam(self, gameData):
        if 'languages' in gameData:
            languages = gameData['languages']
        else:
            languages = None

        if 'genre' in gameData:
            genre = gameData['genre'].split(", ")[0]
        else:
            genre = None
        return {
            'genre': genre,
            'languages': languages
        }


    # Valida se aquele jogo tem uma quantidade mínima de owners
    def validGame(self, game):
        if 'owners' in game:
            owners_str = game['owners']
            owners = self.readOwners(owners_str)
            if owners > 45000:
                return True
            else:
                return False
        else:
            return False

    # Recebe uma string de owners e retorna a média entra elas
    def readOwners(self, str_owners):
        vector_numbers = self.validOwners(str_owners)
        average = self.calculatesAvarege(vector_numbers)
        return average

    # Recebe uma string de owners, as separa em dois inteiros e retorna a media entra elas
    def validOwners(self, str_owners):
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
    def calculatesAvarege(self, numbers):
        sum = 0
        for number in numbers:
            sum = sum + number
        return sum / len(numbers)


# >>>>>>>>>>>>>>>>>> YOUTUBE SECTION <<<<<<<<<<<<<<<<<<<<<<


    def getYoutubeData(self, gameName):
        # Busca o array de ids de videos no youtube relacionados a cada jogo
        arrayIDsYoutubeGame = self.getIDsYoutubeGame(gameName)
        dictionaryGame = {
            # 'id':qtd_jogos,
            'name': gameName,
            'count_videos': len(arrayIDsYoutubeGame),
            'count_views': 0,
            'count_likes': 0,
            'count_dislikes': 0,
            'count_favorites': 0,
            'count_comments': 0
        }
        # Percorre array de ids de videos do youtube
        for id in arrayIDsYoutubeGame:
            videoData = self.getVideoYoutubeData(id)
            print("Requisitando video com ID: {}".format(id))
            print("------------------------------------------")
            dictionaryGame['count_views'] = dictionaryGame['count_views'] + videoData['count_views']
            dictionaryGame['count_likes'] = dictionaryGame['count_likes'] + videoData['count_likes']
            dictionaryGame['count_dislikes'] = dictionaryGame['count_dislikes'] + videoData['count_dislikes']
            dictionaryGame['count_favorites'] = dictionaryGame['count_favorites'] + videoData['count_favorites']
            dictionaryGame['count_comments'] = dictionaryGame['count_comments'] + videoData['count_comments']

        return dictionaryGame


    # Requisita um jogo no youtube e retorna um array com todos os ID's de videos relacionados
    def getIDsYoutubeGame(self, gameName):
        header={'Accept':'application/json'}
        key='AIzaSyDmDXP_gaB7cog4f0slbbdJ3RACsY5WQIw'
        url='https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&q={}GAMEPLAY&key={}'.format(gameName, key)
        request = requests.get(url, headers=header)
        data = request.json()
        return self.filterIDsYoutubeGame(data)

    # Retorna um array com todos os ID's de videos relacionados a um jogo
    def filterIDsYoutubeGame(self, youtubeResults):
        items=[]
        if 'items' in youtubeResults:
            items=youtubeResults['items']

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
    def getVideoYoutubeData(self, idvideo):
        header = {'Accept': 'application/json'}
        key = 'AIzaSyDmDXP_gaB7cog4f0slbbdJ3RACsY5WQIw'
        url = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={}&key={}'.format(idvideo, key)
        request = requests.get(url, headers=header)
        data = request.json()
        return self.filterVideoYoutubeGama(data)

    # Filtra os dados de um video do youtube e retorna um objeto com esses dados
    def filterVideoYoutubeGama(self, video_data):
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

# >>>>>>>>>>>>>>>>>> MERGE SECTION <<<<<<<<<<<<<<<<<<<<<<

        def mergeData(self, steamGame, youtubeGame, twichGame):
            return {
            # Dados Steam
              'name': steamGame['game'],
              'positive_reviews_steam': steamGame['positive_reviews_steam'],
              'negative_reviews_steam': steamGame['negative_reviews_steam'],
              'owners': steamGame['owners'],
              'average_forever': steamGame['average_forever'],
              'average_2weeks': steamGame['average_2weeks'],
              'price': steamGame['price'],
              'languages': steamGame['languages'],
              'genre': steamGame['genre'],
            # Dados Youtube
              'count_videos': youtubeGame['count_videos'],
              'count_views': youtubeGame['count_views'],
              'count_likes': youtubeGame['count_likes'],
              'count_dislikes': youtubeGame['count_dislikes'],
              'count_comments': youtubeGame['count_comments'],
            # Dados Twitch
              'total_views': twichGame['total_views'],
              'streams': twichGame['streams']
            }
