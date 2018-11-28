import unittest
import requests_mock
from . import Steam, Youtube, Twitch, Importer
from PIL import Image


class TestImporter(unittest.TestCase):

    @requests_mock.Mocker()
    def setUp(self, request_mock):
        self.youtube = Youtube.Youtube()
        self.twitch = Twitch.Twitch()
        self.steam = Steam.Steam()

        key = 'AIzaSyDmDXP_gaB7cog4f0slbbdJ3RACsY5WQIw'
        game_name = 'PUBG'
        YOUTUBE_VIDEOS_LIMIT = 2
        url_youtube_id = 'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults={}&q={}GAMEPLAY&key={}'.format(
        YOUTUBE_VIDEOS_LIMIT,
        game_name,
        key,
        )


        data_youtube_id = {
         "kind": "youtube#searchListResponse",
         "etag": "\"XI7nbFXulYBIpL0ayR_gDh3eu1k/bLIY-CLkCHsD4COq-IahYya7RqU\"",
         "nextPageToken": "CAIQAA",
         "regionCode": "BR",
         "pageInfo": {
          "totalResults": 687169,
          "resultsPerPage": 2
         },
         "items": [
          {
           "kind": "youtube#searchResult",
           "etag": "\"XI7nbFXulYBIpL0ayR_gDh3eu1k/FPBk8_z5Bk7Bt4lYzxqVCqV_X14\"",
           "id": {
            "kind": "youtube#video",
            "videoId": "sctOYN2pMs4"
           },
           "snippet": {
            "publishedAt": "2017-12-23T23:00:03.000Z",
            "channelId": "UCIw5rbXUrtk31t20Ap5817w",
            "title": "PlayerUnknown's Battlegrounds (PUBG) Gameplay (PC HD) [1080p60FPS]",
            "description": "PlayerUnknown's Battlegrounds (PUBG) Gameplay (PC HD) [1080p60FPS] Steam Page ...",
            "thumbnails": {
             "default": {
              "url": "https://i.ytimg.com/vi/sctOYN2pMs4/default.jpg",
              "width": 120,
              "height": 90
             },
             "medium": {
              "url": "https://i.ytimg.com/vi/sctOYN2pMs4/mqdefault.jpg",
              "width": 320,
              "height": 180
             },
             "high": {
              "url": "https://i.ytimg.com/vi/sctOYN2pMs4/hqdefault.jpg",
              "width": 480,
              "height": 360
             }
            },
            "channelTitle": "Throneful",
            "liveBroadcastContent": "none"
           }
          },
          {
           "kind": "youtube#searchResult",
           "etag": "\"XI7nbFXulYBIpL0ayR_gDh3eu1k/tcJh9o972j5pkb_sUa2AK9bWQ_c\"",
           "id": {
            "kind": "youtube#video",
            "videoId": "y5i-NqrNvaM"
           },
           "snippet": {
            "publishedAt": "2018-06-27T21:16:12.000Z",
            "channelId": "UCN-v-Xn9S7oYk0X2v1jx1Qg",
            "title": "SOLO SAVAGE - PUBG Gameplay SOLO FPP New Map",
            "description": "Finally played some solos on the new PUBG update and new map (Sanhok, aka \"Savage\")! More gameplays coming soon to my second channel: ...",
            "thumbnails": {
             "default": {
              "url": "https://i.ytimg.com/vi/y5i-NqrNvaM/default.jpg",
              "width": 120,
              "height": 90
             },
             "medium": {
              "url": "https://i.ytimg.com/vi/y5i-NqrNvaM/mqdefault.jpg",
              "width": 320,
              "height": 180
             },
             "high": {
              "url": "https://i.ytimg.com/vi/y5i-NqrNvaM/hqdefault.jpg",
              "width": 480,
              "height": 360
             }
            },
            "channelTitle": "StoneMountain64",
            "liveBroadcastContent": "none"
           }
          }
         ]
        }

        request_mock.get(url_youtube_id, json=data_youtube_id)

        id_video = "y5i-NqrNvaM"
        url_video = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={}&key={}'.format(id_video, key)

        data_video = {
            "kind": "youtube#videoListResponse",
            "etag": "\"XI7nbFXulYBIpL0ayR_gDh3eu1k/lKC5Xzvj3cHi0u0u2F4cBe9Irzs\"",
            "pageInfo": {
            "totalResults": 1,
            "resultsPerPage": 1
            },
            "items": [
                {
                    "kind": "youtube#video",
                    "etag": "\"XI7nbFXulYBIpL0ayR_gDh3eu1k/oKzDIVkNP8fDr7WBj3_BQ1NzeHs\"",
                    "id": "sctOYN2pMs4",
                    "statistics": {
                        "viewCount": "944599",
                        "likeCount": "4485",
                        "dislikeCount": "1423",
                        "favoriteCount": "0",
                        "commentCount": "476"
                    }
                }
            ]
        }

        request_mock.get(url_video, json=data_video)



        game_name = 'PUBG'
        url_twitch = 'https://api.twitch.tv/helix/games?name={}'.format(game_name)
        data_url = {
            "data": [
                {
                    "id": "493057",
                    "name": "PLAYERUNKNOWN'S BATTLEGROUNDS",
                    "box_art_url": "https://static-cdn.jtvnw.net/ttv-boxart/PLAYERUNKNOWN%27S%20BATTLEGROUNDS-{width}x{height}.jpg"
                }
            ]
        }

        request_mock.get(url_twitch, json=data_url)

        game_id = '493057'
        url_id = 'https://api.twitch.tv/helix/streams?game_id={}'.format(game_id)

        data_id = {
            "data": [
                {
                    "id": "31432712304",
                    "user_id": "22159551",
                    "user_name": "Lumi",
                    "game_id": "493057",
                    "community_ids": [
                        "01d41280-9332-4f54-b77a-a20f577beade",
                        "434e0896-4c27-4c87-9275-cbfba2b323f5",
                        "b0e7cf13-4131-4f1b-9810-d88087de024b"
                    ],
                    "type": "live",
                    "title": ":)",
                    "viewer_count": 1032,
                    "started_at": "2018-11-27T21:53:46Z",
                    "language": "en",
                    "thumbnail_url": "https://static-cdn.jtvnw.net/previews-ttv/live_user_lumi-{width}x{height}.jpg",
                    "tag_ids": [
                        "6ea6bca4-4712-4ab9-a906-e3336a9d8039",
                        "ab340187-1794-4630-9eab-e3b75cc86381"
                    ]
                },
                {
                    "id": "31426144768",
                    "user_id": "121652526",
                    "user_name": "LittleBigWhale",
                    "game_id": "493057",
                    "community_ids": [
                        "229f348c-3bdc-45af-8e66-3e7562f7c2a5"
                    ],
                    "type": "live",
                    "title": "Duo ft. Gius",
                    "viewer_count": 602,
                    "started_at": "2018-11-27T14:06:34Z",
                    "language": "fr",
                    "thumbnail_url": "https://static-cdn.jtvnw.net/previews-ttv/live_user_littlebigwhale-{width}x{height}.jpg",
                    "tag_ids": [
                        "6f655045-9989-4ef7-8f85-1edcec42d648"
                    ]
                }
            ]
        }
        request_mock.get(url_id, json=data_id)

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

    def test_get_importadores(self):
        self.importer = Importer.Importer()

        response = self.importer.get()
        self.assertNotEqual(response, None)

    @requests_mock.Mocker()
    def test_get_data_bad(self, request_mock):
        self.importer = Importer.Importer()
        url = 'http://steamspy.com/api.php?request=all'
        data = {}
        datalist = []

        request_mock.get(url, json=data)
        response = self.importer.get()
        self.assertEqual(len(response),0)
