from db.connect_db import Base, engine, SessionLocal
from src.repository.scrap_news import get_all_news
from src.models import News


def create_news():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    news = get_all_news()
    try:
        for item in news:
            title = item['title']
            link = item['link']
            created = item['created']
            category = item['category']
            news = News(title=title, link=link, created=created, category=category)
            session.add(news)
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
    finally:
        session.close()


if __name__ == '__main__':
    create_news()