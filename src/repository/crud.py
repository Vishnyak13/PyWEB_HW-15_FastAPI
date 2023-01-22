from sqlalchemy.orm import Session

from src.models import News
from src.libs.scrapy_news import get_all_news


async def add_all_news(db: Session):
    try:
        news = get_all_news()
        for new in news:
            db.add(News(title=new["title"], link=new["link"], created=new["created"], category=new["category"]))
        db.commit()
        return True
    except Exception as e:
        print(e)
        db.rollback()
    finally:
        db.close()


async def get_news(db: Session):
    try:
        news = db.query(News).all()
        news_list = []
        for new in news:
            news_list.append(
                {"id": new.id, "title": new.title, "link": new.link, "created": new.created, "category": new.category})
        return news_list
    except Exception as e:
        print(e)
    finally:
        db.close()


async def get_news_by_id(id: int, db: Session):
    try:
        news = db.query(News).filter(News.id == id).first()
        return {"id": news.id, "title": news.title, "link": news.link, "created": news.created,
                "category": news.category}
    except Exception as e:
        print(e)


async def delete_news_by_id(id: int, db: Session):
    try:
        news = db.query(News).filter(News.id == id).first()
        if news:
            db.delete(news)
            db.commit()
        return True
    except Exception as e:
        print(e)
        db.rollback()
    finally:
        db.close()
