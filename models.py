from sqlalchemy import Integer, String, Column

from connect_db import Base


class New(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    link = Column(String, unique=True)
    created = Column(String)
    category = Column(String)
