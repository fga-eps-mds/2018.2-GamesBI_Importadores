import unittest
import requests_mock
from . import Steam
from PIL import Image


class TestImporter(unittest.TestCase):


    '''
    @requests_mock.Mocker()
    def test_get_steam_data(self, request_mock):
        self.steam = Steam.Steam()
        url = 'http://steamspy.com/api.php?request=all'
        data = {
            "570":{
        		"appid":570,
        		"name":"Dota 2",
        		"developer":"Valve",
        		"publisher":"Valve",
        		"score_rank":66,
        		"positive":834869,
        		"negative":133650,
        		"userscore":86,
        		"owners":"100,000,000 .. 200,000,000",
        		"average_forever":27248,
        		"average_2weeks":1588,
        		"median_forever":450,
        		"median_2weeks":861,
        		"price":"0",
        		"initialprice":"0",
        		"discount":"0"
            },
        	"578080":{
        		"appid":578080,
        		"name":"PLAYERUNKNOWN'S BATTLEGROUNDS",
        		"developer":"PUBG Corporation",
        		"publisher":"PUBG Corporation",
        		"score_rank":11,
                "positive":467955,
        		"negative":454875,
        		"userscore":49,
        		"owners":"50,000,000 .. 100,000,000",
        		"average_forever":19985,
        		"average_2weeks":701,
        		"median_forever":10766,
        		"median_2weeks":232,
        		"price":"2999",
        		"initialprice":"2999",
        		"discount":"0"
        	}
        }
        request_mock.get(url, json=data)

        response = self.steam.get_steam_data()
        self.assertNotEqual(len(response), 0)
    '''

    def test_get_infos_game_steam(self):
        self.steam = Steam.Steam()
        '''
        url2 = 'https://store.steampowered.com/api/appdetails?appids=570'

        data2 = {
            "570":{
                "success":'true',
                "data":{
                    "type":"game",
                    "name":"Dota 2",
                    "steam_appid":570,
                    "required_age":0,
                    "is_free":'true',
                    "detailed_description":"O jogo mais jogado no Steam",
                    "about_the_game":"<strong>O jogo mais jogado no Steam",
                    "short_description":"Não importa se estão jogando há 10 ou 1.000 horas, sempre há algo de novo para descobrir",
                    "supported_languages":"B\u00falgaro, Tcheco, Dinamarqu\u00eas, Holand\u00eas, Ingl\u00eas<strong>*</strong>, Finland\u00eas, Franc\u00eas, Alem\u00e3o, Grego, H\u00fangaro, Italiano, Japon\u00eas, Coreano<strong>*</strong>, Noruegu\u00eas, Polon\u00eas, Portugu\u00eas, Portugu\u00eas (Brasil), Romeno, Russo, Chin\u00eas simplificado<strong>*</strong>, Espanhol (Espanha), Sueco, Tailand\u00eas, Chin\u00eas tradicional, Turco, Ucraniano<br><strong>*</strong>idiomas com suporte total de \u00e1udio",
                    "reviews":"\u201cUma obra-prima moderna multijogadora.\u201d<br>9.5/10 \u2013 <a href=\"https://www.destructoid.com/review-dota-2-258506.phtml\" target=\"_blank\" rel=\"noreferrer\"  >Destructoid</a><br><br>\u201cQuando se come\u00e7a a aprender os segredos, descobre-se que as diversas formas de se jogar s\u00e3o inigual\u00e1veis, mesmo por outros jogos do g\u00eanero.\u201d<br>9.4/10 \u2013 <a href=\"http://www.ign.com/articles/2013/07/24/dota-2-review\" target=\"_blank\" rel=\"noreferrer\"  >IGN</a><br><br>\u201cDota 2 \u00e9 possivelmente o \u00fanico jogo competitivo gratuito para jogar cuja jogabilidade n\u00e3o \u00e9 afetada pela forma de monetiza\u00e7\u00e3o.\u201d<br>90/100 \u2013 <a href=\"http://www.pcgamer.com/dota-2-review-2/\" target=\"_blank\" rel=\"noreferrer\"  >PC Gamer</a><br>",
                    "header_image":"https://steamcdn-a.akamaihd.net/steam/apps/570/header.jpg?t=1541701921",
                    "website":"http://www.dota2.com/",
                    "pc_requirements":{
                        "minimum":"<strong>M\u00ednimos:</strong><br><ul class=\"bb_ul\"><li><strong>SO:</strong> Windows 7 or newer<br></li><li><strong>Processador:</strong> Dual core from Intel or AMD at 2.8 GHz<br></li><li><strong>Mem\u00f3ria:</strong> 4 GB de RAM<br></li><li><strong>Placa de v\u00eddeo:</strong> nVidia GeForce 8600/9600GT, ATI/AMD Radeon HD2600/3600<br></li><li><strong>DirectX:</strong> Vers\u00e3o 9.0c<br></li><li><strong>Rede:</strong> Conex\u00e3o de internet banda larga<br></li><li><strong>Armazenamento:</strong> 15 GB de espa\u00e7o dispon\u00edvel<br></li><li><strong>Placa de som:</strong> DirectX Compatible</li></ul>"
                    },
                    "mac_requirements":{
                        "minimum":"<strong>M\u00ednimos:</strong><br><ul class=\"bb_ul\"><li><strong>SO:</strong> OS X Mavericks 10.9 or newer<br></li><li><strong>Processador:</strong> Dual core from Intel<br></li><li><strong>Mem\u00f3ria:</strong> 4 GB de RAM<br></li><li><strong>Placa de v\u00eddeo:</strong> nVidia 320M or higher, or Radeon HD 2400 or higher, or Intel HD 3000 or higher<br></li><li><strong>Rede:</strong> Conex\u00e3o de internet banda larga<br></li><li><strong>Armazenamento:</strong> 15 GB de espa\u00e7o dispon\u00edvel</li></ul>"
                    },
                    "linux_requirements":{
                        "minimum":"<strong>M\u00ednimos:</strong><br><ul class=\"bb_ul\"><li><strong>SO:</strong> Ubuntu 12.04 or newer<br></li><li><strong>Processador:</strong> Dual core from Intel or AMD at 2.8 GHz<br></li><li><strong>Mem\u00f3ria:</strong> 4 GB de RAM<br></li><li><strong>Placa de v\u00eddeo:</strong> nVidia Geforce 8600/9600GT (Driver v331), AMD HD 2xxx-4xxx (Driver mesa 10.5.9), AMD HD 5xxx+ (Driver mesa 10.5.9 or Catalyst 15.7), Intel HD 3000 (Driver mesa 10.6)<br></li><li><strong>Rede:</strong> Conex\u00e3o de internet banda larga<br></li><li><strong>Armazenamento:</strong> 15 GB de espa\u00e7o dispon\u00edvel<br></li><li><strong>Placa de som:</strong> OpenAL Compatible Sound Card</li></ul>"
                    },
                    "developers":["Valve"],
                    "publishers":["Valve"],
                    "packages":[197846],
                    "package_groups":[
                        {
                            "name":"default",
                            "title":"Comprar Dota 2",
                            "description":"",
                            "selection_text":"Selecione uma op\u00e7\u00e3o de compra",
                            "save_text":"","display_type":0,
                            "is_recurring_subscription":"false",
                            "subs":[
                                {
                                    "packageid":197846,
                                    "percent_savings_text":"",
                                    "percent_savings":0,
                                    "option_text":"Dota 2 - Commercial License - Gratuito",
                                    "option_description":"",
                                    "can_get_free_license":"0",
                                    "is_free_license":'true',
                                    "price_in_cents_with_discount":0
                                }
                            ]
                        }
                    ],
                    "platforms":{
                        "windows":'true',
                        "mac":'true',
                        "linux":'true'
                    },"metacritic":{
                        "score":90,
                        "url":"https://www.metacritic.com/game/pc/dota-2?ftag=MCD-06-10aaa1f"
                    },
                    "categories":[
                        {
                            "id":1,
                            "description":"Multijogador"
                        },
                        {
                            "id":9,
                            "description":"Cooperativo"
                        },
                        {
                            "id":29,
                            "description":"Cartas Colecion\u00e1veis Steam"
                        },
                        {
                            "id":30,
                            "description":"Oficina Steam"
                        },
                        {
                            "id":40,
                            "description":"Colecion\u00e1veis do SteamVR"
                        },
                        {
                            "id":35,
                            "description":"Compras em aplicativo"
                        },
                        {
                            "id":8,
                            "description":"Usa Valve Antitrapa\u00e7a"
                        }
                    ],
                    "genres":[
                        {
                            "id":"1",
                            "description":"A\u00e7\u00e3o"
                        },
                        {
                            "id":"37",
                            "description":"Gratuitop/Jogar"
                        },
                        {
                            "id":"2",
                            "description":"Estrat\u00e9gia"
                        }
                    ],
                    "screenshots":[
                        {
                            "id":0,
                            "path_thumbnail":"https://steamcdn-a.akamaihd.net/steam/apps/570/ss_86d675fdc73ba10462abb8f5ece7791c5047072c.600x338.jpg?t=1541701921",
                            "path_full":"https://steamcdn-a.akamaihd.net/steam/apps/570/ss_86d675fdc73ba10462abb8f5ece7791c5047072c.1920x1080.jpg?t=1541701921"
                        },
                    ],
                    "movies":[
                        {
                            "id":256692021,
                            "name":"Dota 2 - Join the Battle",
                            "thumbnail":"https://steamcdn-a.akamaihd.net/steam/apps/256692021/movie.293x165.jpg?t=1501892790",
                            "webm":{
                                "480":"http://steamcdn-a.akamaihd.net/steam/apps/256692021/movie480.webm?t=1501892790",
                                "max":"http://steamcdn-a.akamaihd.net/steam/apps/256692021/movie_max.webm?t=1501892790"
                            },
                            "highlight":'true'
                        },
                    ],
                    "recommendations":{
                        "total":15634
                    },
                    "release_date":{
                        "coming_soon":'false',
                        "date":"9/jul/2013"
                    },
                    "support_info":{
                        "url":"http://dev.dota2.com/",
                        "email":""
                    },
                    "background":"https://steamcdn-a.akamaihd.net/steam/apps/570/page_bg_generated_v6b.jpg?t=1541701921",
                    "content_descriptors":{
                        "ids":[],
                        "notes":'null'
                    }
                }
            }
        }
        request_mock.get(url2, json=data2)

        url3 = 'https://steamcdn-a.akamaihd.net/steam/apps/570/ss_86d675fdc73ba10462abb8f5ece7791c5047072c.600x338.jpg?t=1541701921'

        im = Image.open('imgTest.jpg')
        request_mock.get(url3, json=im)

        '''
        game_id = 570

        response = self.steam.get_infos_game_steam(game_id)
        self.assertNotEqual(response, None)

    def test_get_infos_game_steam_Bad_Request(self):
        self.steam = Steam.Steam()

        game_id = 570154
        data = {
            'r_average': None,
            'g_average': None,
            'b_average': None,
            'main_image': None,
            'languages': [],
            'genres': [],
            'screenshots': [],
            'release_date': None
        }

        response = self.steam.get_infos_game_steam(game_id)
        self.assertEqual(response, data)

    @requests_mock.Mocker()
    def test_get_steam_data_bad(self, request_mock):
        self.steam = Steam.Steam()
        url = 'http://steamspy.com/api.php?request=all'
        data = {}
        datalist = []

        request_mock.get(url, json=data)
        response = self.steam.get_steam_data()
        self.assertEqual(response,datalist)

if __name__ == '__main__':
    unittest.main()
