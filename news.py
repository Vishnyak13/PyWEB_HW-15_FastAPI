import json

from fastapi import HTTPException

from connect_db import SessionLocal
from models import New


def get_all_news():
    with SessionLocal() as session:
        news = session.query(New).all()
        news_list = []
        for n in news:
            news_dict = {}
            news_dict['id'] = n.id
            news_dict['title'] = n.title
            news_dict['link'] = n.link
            news_dict['created'] = n.created
            news_dict['category'] = n.category
            news_list.append(news_dict)
    new_json = json.dumps(news_list)
    return new_json

