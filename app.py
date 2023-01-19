import json

from fastapi import FastAPI, HTTPException, status
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
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database is not responding")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error connecting to database')


@app.get("/")
def root():
    return RedirectResponse(url='/docs')


@app.get("/news/", status_code=status.HTTP_200_OK, response_model=NewsList)
def get_news():
    result = news.get_all_news()
    result = json.loads(result)
    all_news = [News(**item) for item in result]
    return NewsList(news=all_news)


@app.get("/news/{id}", status_code=status.HTTP_200_OK, response_model=News)
def get_news_by_id(id: int):
    result = news.get_news_by_id(id)
    result = json.loads(result)
    return News(**result)


@app.get("/news/category/{category}", status_code=status.HTTP_200_OK, response_model=NewsList)
def get_news_by_category(category: str):
    result = news.get_news_by_category(category)
    result = json.loads(result)
    all_news = [News(**item) for item in result]
    return NewsList(news=all_news)


@app.post("/news/", status_code=status.HTTP_201_CREATED, response_model=News)
def add_one_new(body: NewsBase):
    title = body.title
    link = body.link
    created = body.created
    category = body.category
    news_id = news.add_new(title, link, created, category)
    result = news.get_news_by_id(news_id)
    result = json.loads(result)
    return News(**result)


@app.delete("/news/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one_new(id: int):
    answer = news.delete_news(id)
    if answer == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="News not found")
    else:
        return {"message": "News {} was deleted".format(id)}
