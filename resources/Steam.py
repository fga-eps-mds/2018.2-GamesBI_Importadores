from flask_restful import Resource
from flask import jsonify
import requests
from pprint import pprint

class Steam(Resource):
    def get(self):
        request = requests.get('http://steamspy.com/api.php?request=appdetails&appid=730')
        return request.json()
