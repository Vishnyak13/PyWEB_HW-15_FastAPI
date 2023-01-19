from typing import List

from fastapi import FastAPI, Depends
import json

from starlette.responses import RedirectResponse

from db.connect_db import SessionLocal, get_db
from src import schemas
from src.repository import news as news_repository

app = FastAPI()


@app.get("/healthcheck")
def healthcheck():
    return {"status": "Everything is OK"}


@app.get("/")
def main():
    return RedirectResponse(url='/docs')


@app.get("/news/", status_code=200, response_model=List[schemas.News])
def read_all_news(skip: int = 0, limit: int = 100, db: SessionLocal = Depends(get_db)):
    news = news_repository.get_all_news(db, skip=skip, limit=limit)
    return news
