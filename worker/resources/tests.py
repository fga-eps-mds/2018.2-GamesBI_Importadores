from Youtube import Youtube
from Twitch import Twitch
from Steam import Steam
import unittest


class TestImporter(unittest.TestCase):

	def setUp(self):
		self.data_name = "Counter Strike"
		self.steam = Steam()
		self.youtube = Youtube()
		self.twitch = Twitch()


	def test_status_code_Steam(self):
		response = self.steam.get_steam_data()
		self.assertNotEqual(len(response), 0)




if __name__ == '__main__':
    unittest.main()
