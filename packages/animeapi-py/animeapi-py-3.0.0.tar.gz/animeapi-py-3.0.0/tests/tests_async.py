import unittest
from datetime import datetime

import animeapi


class TestSyncAnimeAPI(unittest.IsolatedAsyncioTestCase):
    """Test the AsyncAnimeAPI class"""

    async def test_v2(self):
        """Test the AsyncAnimeAPI class with v2"""
        api = animeapi.AsyncAnimeAPI(base_url=animeapi.Version.V2)
        updated = await api.get_updated_time()
        await api.close()
        self.assertIsInstance(updated, str)

    async def test_v3_variable(self):
        """Test the AsyncAnimeAPI class with v3"""
        api = animeapi.AsyncAnimeAPI()
        status = await api.get_status()
        await api.close()
        self.assertIsInstance(status, animeapi.ApiStatus)

    async def test_v3_with_context(self):
        """Test the AsyncAnimeAPI class with v3"""
        async with animeapi.AsyncAnimeAPI() as api:
            status = await api.get_updated_time(use_datetime=True)
            self.assertIsInstance(status, datetime)

    async def test_single_anime(self):
        """Test the AsyncAnimeAPI class with a single anime"""
        api = animeapi.AsyncAnimeAPI()
        anime = await api.get_anime_relations(1, animeapi.Platform.MAL)
        await api.close()
        print(anime)
        self.assertIsInstance(anime, animeapi.AnimeRelation)

    async def test_multiple_anime_dict(self):
        """Test the AsyncAnimeAPI class with multiple anime as a dict"""
        api = animeapi.AsyncAnimeAPI()
        anime = await api.get_dict_anime_relations(animeapi.Platform.OTAKOTAKU)
        await api.close()
        print(anime["1"])
        self.assertIsInstance(anime, dict)

    async def test_multiple_anime_list(self):
        """Test the AsyncAnimeAPI class with multiple anime as a list"""
        api = animeapi.AsyncAnimeAPI()
        anime = await api.get_list_anime_relations(animeapi.Platform.ANIMEPLANET)
        await api.close()
        print(anime[0])
        self.assertIsInstance(anime, list)

    async def test_get_index(self):
        """Test the AsyncAnimeAPI class with get_index"""
        api = animeapi.AsyncAnimeAPI()
        index = await api.get_list_index()
        await api.close()
        print(index[0])
        self.assertIsInstance(index, list)

    async def test_get_hearbeat(self):
        """Test the AsyncAnimeAPI class with get_heartbeat"""
        api = animeapi.AsyncAnimeAPI()
        heartbeat = await api.get_heartbeat()
        await api.close()
        self.assertIsInstance(heartbeat, animeapi.Heartbeat)


if __name__ == "__main__":
    unittest.main()