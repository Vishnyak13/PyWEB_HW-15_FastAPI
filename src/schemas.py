from typing import List

from pydantic import BaseModel


class NewsBase(BaseModel):
    title: str
    link: str
    created: str
    category: str


class News(NewsBase):
    news_id: str


class NewsList(BaseModel):
    news: List[News]