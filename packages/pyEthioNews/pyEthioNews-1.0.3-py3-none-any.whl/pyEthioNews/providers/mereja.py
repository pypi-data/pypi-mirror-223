from typing import List

from pyEthioNews.news import AsyncBaseScraper
from pyEthioNews.types import News


class Mereja(AsyncBaseScraper):
    def __init__(self):
        super().__init__()
        self.url = "https://www.merega.com/"

    async def get_news(
        self,
        limit: int = 10,
        *args,
        **kwargs,
    ) -> List[News]:
        url = (
            "http://mereja.com/amharic/v2/wp-json/wp/v2/posts"
            + "?per_page="
            + str(limit)
        )
        return await self._fetch_news(url)

    async def get_news_by_id(self, id_: int) -> News:
        url = self.url + "wp-json/wp/v2/posts/{}".format(id_)
        return await self._fetch_news(url)
