from typing import Optional, List

from pyEthioNews.types import NewsType, News
from pyEthioNews.news import AsyncBaseScraper


class FanaBc(AsyncBaseScraper):
    def __init__(self):
        super().__init__()
        self.url = "https://www.fanabc.com/"
        self.categorises = {
            "business": 55,
            "sport": 56,
        }

    async def get_main_news(
        self,
        limit: int = 10,
    ) -> List[News]:
        url = self.url + "wp-json/wp/v2/posts" + "?per_page=" + str(limit)
        return await self._fetch_news(url)

    async def get_business_news(
        self,
        limit: int = 10,
    ) -> List[News]:
        url = self.get_url(self.categorises["business"], limit)
        return await self._fetch_news(url)

    async def get_sport_news(
        self,
        limit: int = 10,
    ) -> List[News]:
        url = self.get_url(self.categorises["sport"], limit)
        return await self._fetch_news(url)

    async def get_news_by_id(self, id_: int) -> News:
        url = self.url + "wp-json/wp/v2/posts/{}".format(id_)
        return await self._fetch_news(url)

    async def get_news(
        self,
        limit: int = 10,
        news: Optional[News] = NewsType.LOCAL,
    ) -> List[News]:
        if news == NewsType.LOCAL:
            return await self.get_main_news(limit)

        elif news == NewsType.WORLD_WIDE:
            return await self.get_main_news(limit)

        elif news == NewsType.BUSINESS:
            return await self.get_business_news(limit)

        elif news == NewsType.SPORT:
            return await self.get_sport_news(limit)
