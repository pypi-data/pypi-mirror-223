import json
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from bs4 import BeautifulSoup

from pyEthioNews.news import AsyncBaseScraper


@dataclass
class VoaNews:
    link: str
    title: str
    image: str
    date: str
    _client: "VOAAmharic" = None

    async def fetch(self) -> "VoaNewsDetail":
        if not self._client:
            raise ValueError("You must set a client")
        return await self._client.fetch_news(self)


@dataclass
class VoaNewsDetail:
    title: str
    image: str
    date: datetime
    html: str
    modified: Optional[datetime] = None

    @property
    def content(self):
        return BeautifulSoup(self.html, "html.parser").text

    def dict(self):
        return {
            "title": self.title,
            "image": self.image,
            "date": self.date.isocalendar(),
            "content": self.content,
            "modified": self.modified.isocalendar() if self.modified else None,
        }


class VOAAmharic(AsyncBaseScraper):
    def __init__(self):
        super().__init__()
        self.url = "https://amharic.voanews.com/{}"

    async def get_world_wide_news(self, page: Optional[int] = 0) -> List[VoaNews]:
        res = await self._s.get(self.url.format("z/3737"), params={"p": page})
        return self._fetch_news_form_html(res.text)

    def _fetch_news_form_html(self, html: str) -> List[VoaNews]:
        soup = self._soup(html)
        div = soup.find_all("div", class_="media-block")
        return [
            VoaNews(
                link=i.find("a")["href"],
                title=i.find("h4").get_text(strip=True),
                image=i.find("img", {"data-src": True})["data-src"],
                date=i.find("span", class_="date").text,
                _client=self,
            )
            for i in div
        ]

    def _fetch_details_from_html(self, html: str) -> VoaNewsDetail:
        soup = self._soup(html)
        title = soup.find("title").text
        content = soup.find("div", class_="wsw")
        content = soup.find(
            "div", class_="media-pholder media-pholder--video"
        ).prettify() if not content else content.prettify()
        json_data = json.loads(
            soup.find("script", {"type": "application/ld+json"}).string
        )
        date_published = json_data["datePublished"]
        date_modified = json_data["dateModified"]
        image = json_data["image"]["url"]
        return VoaNewsDetail(
            title=title,
            image=image,
            date=datetime.strptime(date_published, "%Y-%m-%d"),
            html=content,
            modified=datetime.strptime(date_modified, "%Y-%m-%d %H:%M:%SZ"),
        )

    async def fetch_news(self, news: VoaNews) -> VoaNewsDetail:
        res = await self._s.get(self.url.format(news.link))
        return self._fetch_details_from_html(res.text)

    async def get(self, slug: str) -> VoaNewsDetail:
        res = await self._s.get(self.url.format(slug))
        return self._fetch_details_from_html(res.text)

    async def search(self, query: str, page: int = 1, limit: int = 10) -> List[VoaNews]:
        res = await self._s.get(
            self.url.format("s"),
            params={"k": query, "tab": "all", "pi": page, "r": "any", "pp": limit},
        )
        return self._fetch_news_form_html(res.text)
