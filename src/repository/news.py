from sqlalchemy.orm import Session
from src.models import News


def get_all_news(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(News).offset(skip).limit(limit).all()
    except Exception as e:
        print(e)
        return []
