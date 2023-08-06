import html
import json
import re
from datetime import datetime
from enum import Enum
from typing import Dict, Any

import httpx
from bs4 import BeautifulSoup


class WaltaNewsType(Enum):
    NEWS = "News"
    ECONOMY = "Economy"
    POLITICS = "Politics"
    SOCIAL = "Social"


class WaltaSportNewsType(Enum):
    FOOTBALL = "Football"
    LOCAL = "Social"
    INTERNATIONAL = "International"


class Author:
    def __init__(self, data: Dict[str, Any]):
        self.name = data["name"]
        self.slug = data["slug"]
        self.id_ = data.get("ID") or data.get("id")


class NewsType(Enum):
    LOCAL = "Local"
    WORLD_WIDE = "World"
    BUSINESS = "Business"
    SPORT = "Sport"


class Categories:
    def __init__(self, data: Dict[str, Any]):
        self.name = data["name"]
        self.slug = data["slug"]
        self.id_ = data.get("ID") or data.get("id")


class News:
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.id_ = data["id"]
        self.date = data["date"]
        self.slug = data["slug"]
        self.modified = data["modified"]
        self.domain = re.findall(r"^(?:https|http):\/\/(.*.com)\/", data["link"])[0]
        self.url = data["link"]
        self.title = data["title"]["rendered"].replace("&#8211;", "-")
        self.content = data["content"]["rendered"]
        self.excerpt = data["excerpt"]["rendered"].replace("&#8211;", "-")
        self.author = Author(data.get("pwapp_author"))
        self.pwapp_terms = data.get("pwapp_terms")
        self.categories = (
            data["pwapp_terms"]["category"]
            if self.pwapp_terms
            else self.data["categories"]
        )
        self.tags = data["tags"]
        self.comment_status = data["comment_status"]
        self.format = data["format"]
        self.status = data["status"]
        self.image = (
            data.get("share_image")
            if not data.get("featured_image")
            else data["featured_image"]
        )
        self.clean_title()

    def clean_content(self):
        soup = BeautifulSoup(self.content, "lxml")
        return html.unescape(soup.text).replace("&#8211;", "-")

    def get_image(self):
        if not self.image:
            soup = BeautifulSoup(self.content)
            return soup.find("img")["src"]
        return self.image["source"]

    async def get_author(self):
        if not self.author:
            author = self.data["author"]
            url = (
                "https://"
                + self.domain
                + "/amharic/v2/wp-json/wp/v2/users/"
                + str(author)
            )
            s = httpx.AsyncClient()
            res = await s.get(url)
            results_json = json.loads(res.text)
            await s.aclose()
            return Author(results_json)
        return Author(self.author)

    def clean_excerpt(self):
        soup = BeautifulSoup(self.excerpt, "lxml")
        return html.unescape(soup.text).replace("&#8211;", "-")

    def clean_title(self):
        return html.unescape(self.title).replace("&#8211;", "-")

    def convert_date(self):
        return datetime.strptime(self.date, "%Y-%m-%dT%H:%M:%S").timestamp()

    async def get_category(self):
        if not self.categories:
            url = (
                "https://"
                + self.domain
                + "/amharic/v2/wp-json/wp/v2/categories?post="
                + str(self.id_)
            )
            s = httpx.AsyncClient()
            res = await s.get(url)
            results_json = json.loads(res.text)
            await s.aclose()
            return [Categories(cat) for cat in results_json]
        return [Categories(cat) for cat in self.categories]

    def convert_modified_date(self):
        return datetime.strptime(self.modified, "%Y-%m-%dT%H:%M:%S").timestamp()
