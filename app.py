import json
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from connect_db import SessionLocal
import news
from schemas import NewsList, NewsBase, News

app = FastAPI()


@app.get("/healthcheck")
def healthcheck():
    db = SessionLocal()
    try:
        r = db.execute("SELECT 1").fetchone()
        if r is None:
            raise HTTPException(status_code=500, detail="Database is not responding")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Error connecting to database')


@app.get("/")
def root():
    return RedirectResponse(url='/docs')


@app.get("/news/", status_code=200, response_model=NewsList)
def get_news():
    result = news.get_all_news()
    result = json.loads(result)
    all_news = [News(**item) for item in result]
    return NewsList(news=all_news)


