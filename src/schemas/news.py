from typing import List

from pydantic import BaseModel


class NewsBase(BaseModel):
    title: str
    link: str
    created: str
    category: str


class NewsResponse(NewsBase):
    id: int


class NewsList(BaseModel):
    news: List[NewsResponse]