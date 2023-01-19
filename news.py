import json

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


def get_news_by_id(id):
    with SessionLocal() as session:
        news = session.query(New).filter(New.id == id).first()
        new_dict = {}
        new_dict['id'] = news.id
        new_dict['title'] = news.title
        new_dict['link'] = news.link
        new_dict['created'] = news.created
        new_dict['category'] = news.category
    new_json = json.dumps(new_dict)
    return new_json


def get_news_by_category(category):
    with SessionLocal() as session:
        news = session.query(New).filter(New.category == category).all()
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


def add_new(title, link, created, category):
    with SessionLocal() as session:
        news = New(title=title, link=link, created=created, category=category)
        session.add(news)
        session.commit()
        news_id = session.query(New).filter(New.title == title).first().id
    return news_id


def delete_news(id):
    with SessionLocal() as session:
        news = session.query(New).filter(New.id == id).first()
        if news:
            session.delete(news)
            session.commit()
            return True
        else:
            return False
