import unittest
import requests_mock
from . import Youtube, Twitch, Steam


class TestImporter(unittest.TestCase):

	@requests_mock.Mocker()
	def setUp(self, request_mock):
		self.data_name = "Counter Strike"
		self.steam = Steam()
		self.youtube = Youtube()
		self.twitch = Twitch()
		self.importer = Importer()


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


	def test_requisicao_id_Yotube(self):

		response = self.youtube.get_ids_youtube_game(self, game_name)
		self.assertNotEqual(len(response), 0)

	@requests_mock.Mocker()
	def test_requisicao_video_Yotube(self, request_mock):
		id_video1 = "sctOYN2pMs4"
		id_video2 = "y5i-NqrNvaM"
		url = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id=={}&key={}'.format(id_video1, key)
		url2 = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={}&key={}'.format(id_video2, key)

		data_video1 = {
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
		    "viewCount": "907581",
		    "likeCount": "4067",
		    "dislikeCount": "1352",
		    "favoriteCount": "0",
		    "commentCount": "466"
		   }
		  }
		 ]
		}
		request_mock.get(url, json=data_video1)

		data_video2 = {
		 "kind": "youtube#videoListResponse",
		 "etag": "\"XI7nbFXulYBIpL0ayR_gDh3eu1k/W0vax7Wv9-3oO0UY9LIyL7zRqRc\"",
		 "pageInfo": {
		  "totalResults": 1,
		  "resultsPerPage": 1
		 },
		 "items": [
		  {
		   "kind": "youtube#video",
		   "etag": "\"XI7nbFXulYBIpL0ayR_gDh3eu1k/hkFkADlY2L0pqmzl8whDsZT-Y48\"",
		   "id": "y5i-NqrNvaM",
		   "statistics": {
		    "viewCount": "351464",
		    "likeCount": "5045",
		    "dislikeCount": "102",
		    "favoriteCount": "0",
		    "commentCount": "345"
		   }
		  }
		 ]
		}
		request_mock.get(url2, json=data_video2)

		data_None = {
			'name': game_name,
			'count_videos': None,
			'count_views': None,
			'count_likes': None,
			'count_dislikes': None,
			'count_favorites': None,
			'count_comments': None
		}

		array_ids_youtube = self.youtube.get_ids_youtube_game(self, game_name)
		for id in array_ids_youtube:
			video_data = self.youtube.get_video_youtube_data(id)
			self.assertNotEqual(video_data, data_None)


if __name__ == '__main__':
    unittest.main()
