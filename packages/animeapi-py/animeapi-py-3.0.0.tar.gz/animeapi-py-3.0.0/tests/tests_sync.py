import unittest

import animeapi


class TestSyncAnimeAPI(unittest.TestCase):
    """Test the AnimeAPI class"""

    def test_v2(self):
        """Test the AnimeAPI class with v2"""
        api = animeapi.AnimeAPI(base_url=animeapi.Version.V2)
        updated = api.get_updated_time()
        self.assertIsInstance(updated, str)

    def test_v3(self):
        """Test the AnimeAPI class with v3"""
        api = animeapi.AnimeAPI()
        status = api.get_status()
        self.assertIsInstance(status, animeapi.ApiStatus)

    def test_single_anime(self):
        """Test the AnimeAPI class with a single anime"""
        api = animeapi.AnimeAPI()
        anime = api.get_anime_relations(1, animeapi.Platform.MAL)
        print(anime)
        self.assertIsInstance(anime, animeapi.AnimeRelation)

    def test_multiple_anime_dict(self):
        """Test the AnimeAPI class with multiple anime as a dict"""
        api = animeapi.AnimeAPI()
        anime = api.get_dict_anime_relations(animeapi.Platform.OTAKOTAKU)
        print(anime["1"])
        self.assertIsInstance(anime, dict)

    def test_multiple_anime_list(self):
        """Test the AnimeAPI class with multiple anime as a list"""
        api = animeapi.AnimeAPI()
        anime = api.get_list_anime_relations(animeapi.Platform.ANIMEPLANET)
        print(anime[0])
        self.assertIsInstance(anime, list)

    def test_get_index(self):
        """Test the AnimeAPI class with get_index"""
        api = animeapi.AnimeAPI()
        index = api.get_list_index()
        print(index[0])
        self.assertIsInstance(index, list)

    def test_get_hearbeat(self):
        """Test the AnimeAPI class with get_heartbeat"""
        api = animeapi.AnimeAPI()
        heartbeat = api.get_heartbeat()
        self.assertIsInstance(heartbeat, animeapi.Heartbeat)


if __name__ == "__main__":
    unittest.main()