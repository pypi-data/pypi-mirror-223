import json
from typing import Union, List, Optional
import httpx
from bs4 import BeautifulSoup
from .types import News


class AsyncBaseScraper:
    def __init__(self):
        self._url = None
        self._headers = {"User-Agent": "Mozilla/5.0"}
        self._s = httpx.AsyncClient(follow_redirects=True)

    @staticmethod
    def _soup(html: str) -> BeautifulSoup:
        return BeautifulSoup(html, "html.parser")

    async def _fetch_news(self, url: str) -> Union[List[News], News]:
        r = await self._s.get(url, headers=self._headers)
        results_json = json.loads(r.text)
        if isinstance(results_json, dict):
            news = News(results_json)
            return news
        news = []
        for result in results_json:
            news.append(News(result))
        return news

    def get_url(self, news_id: int, limit: Optional[Union[int, str]] = None) -> str:
        if limit:
            return (
                f"{self._url}wp-json/wp/v2/posts?categories={news_id}&per_page={limit}"
            )
        return f"{self._url}wp-json/wp/v2/posts?categories={news_id}"
