from typing import Union, Optional, List
from pyEthioNews.news import AsyncBaseScraper
from pyEthioNews.types import WaltaNewsType, WaltaSportNewsType, News, NewsType


class Walta(AsyncBaseScraper):
    def __init__(self):
        super().__init__()
        self.url = "https://waltainfo.com/"
        self.categorises = {
            "local": {
                WaltaNewsType.NEWS.value: 158,
                WaltaNewsType.ECONOMY.value: 162,
                WaltaNewsType.POLITICS.value: 160,
                WaltaNewsType.SOCIAL.value: 158,
            },
            "africa": {
                WaltaNewsType.NEWS.value: 167,
                WaltaNewsType.ECONOMY.value: 169,
                WaltaNewsType.POLITICS.value: 171,
                WaltaNewsType.SOCIAL.value: 173,
            },
            "world": {
                WaltaNewsType.NEWS.value: 177,
                WaltaNewsType.ECONOMY.value: 179,
                WaltaNewsType.POLITICS.value: 181,
                WaltaNewsType.SOCIAL.value: 183,
            },
            "sport": {
                WaltaSportNewsType.FOOTBALL.value: 199,
                WaltaSportNewsType.LOCAL.value: 352,
                WaltaSportNewsType.INTERNATIONAL.value: 350,
            },
        }

    async def get_local_news(
        self, limit: int = 10, type_: Optional[WaltaNewsType] = WaltaNewsType.NEWS
    ) -> List[News]:
        url = self.get_url(self.categorises["local"][type_.value], limit)
        return await self._fetch_news(url)

    async def get_africa_news(
        self, limit: int = 10, type_: Optional[WaltaNewsType] = WaltaNewsType.NEWS
    ) -> List[News]:
        url = self.get_url(self.categorises["africa"][type_.value], limit)
        return await self._fetch_news(url)

    async def get_world_wide_news(
        self, limit: int = 10, type_: Optional[WaltaNewsType] = WaltaNewsType.NEWS
    ) -> List[News]:
        url = self.get_url(self.categorises["world"][type_.value], limit)
        return await self._fetch_news(url)

    async def get_sport_news(
        self,
        limit: int = 10,
        type_: Optional[WaltaSportNewsType] = WaltaSportNewsType.FOOTBALL,
    ) -> List[News]:
        url = self.get_url(self.categorises["sport"][type_.value], limit)
        return await self._fetch_news(url)

    async def get_business_news(self, limit: int = 10) -> List[News]:
        url = (
            self.url + "wp-json/wp/v2/posts?categories=303" + "&per_page=" + str(limit)
        )
        return await self._fetch_news(url)

    async def get_news_by_id(self, id_: int) -> News:
        url = self.url + "wp-json/wp/v2/posts/{}".format(id_)
        return await self._fetch_news(url)

    async def get_news(
        self,
        type_: Optional[Union[WaltaNewsType, WaltaSportNewsType]] = None,
        limit: int = 10,
        news: Optional[News] = NewsType.LOCAL,
    ) -> List[News]:
        if type_ is None:
            type_ = WaltaNewsType.NEWS

        if news == NewsType.LOCAL:
            return await self.get_local_news(limit, type_)

        elif news == NewsType.WORLD_WIDE:
            return await self.get_world_wide_news(limit, type_)

        elif news == NewsType.BUSINESS:
            return await self.get_business_news(limit)

        elif news == NewsType.SPORT:
            if not type_ or not isinstance(type_, WaltaSportNewsType):
                type_ = WaltaSportNewsType.FOOTBALL
            return await self.get_sport_news(limit, type_)
