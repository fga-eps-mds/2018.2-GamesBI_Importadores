from flask_restful import Resource
# from flask import jsonify
import requests
# from pprint import pprint


class Steam(Resource):

    def get(self):
        url = 'http://steamspy.com/api.php?request=all'
        header = {'Accept': 'application/json'}
        request = requests.get(url, headers=header)
        data = request.json()
        return self.filterGamesData(data)

    # This method return a array of select games
    def filterGamesData(self, gamesData):
        selectGames = []
        for game in gamesData.values():
            if self.validGame(game):
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
                    'price': price
                }
                selectGames.append(filtered_data)
        return selectGames

    # This method define the select games
    # using a number of mean owners
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

    # This method read the string owners
    # end return the mean of them
    def readOwners(self, str_owners):
        vector_numbers = self.validOwners(str_owners)
        average = self.calculatesAvarege(vector_numbers)
        return average

    # This method reads a owners string,
    # and separates it into two integers
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

    # This method takes a vector of numbers and
    # calculates the mean between them
    def calculatesAvarege(self, numbers):
        sum = 0
        for number in numbers:
            sum = sum + number
        return sum / len(numbers)
