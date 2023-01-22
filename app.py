from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from db.connect_db import get_db
from src.repository.crud import add_all_news, get_news, get_news_by_id, delete_news_by_id
from src.schemas.news import NewsBase, NewsList, NewsResponse

app = FastAPI()


@app.get("/healthchecker")
async def healthchecker(db: Session = Depends(get_db)):
    try:
        r = db.execute("SELECT 1").fetchone()
        if r is None:
            raise HTTPException(status_code=500, detail="Database is not responding")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error connecting to database')


@app.get("/")
def root():
    return RedirectResponse(url="/docs")


@app.post("/add_news", status_code=status.HTTP_201_CREATED)
async def add_news_to_db(db: Session = Depends(get_db)):
    try:
        r = await add_all_news(db)
        if r is not True:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="News not found")
        return {"message": "News added successfully"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error adding news to database')


@app.get("/get_news", response_model=List[NewsResponse])
async def get_news_from_db(db: Session = Depends(get_db)):
    try:
        r = await get_news(db)
        if r is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="News not found")
        return r
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Error getting news from database')


@app.get("/get_news/{id}", response_model=NewsResponse)
async def get_news_by_id_from_db(id: int, db: Session = Depends(get_db)):
    try:
        r = await get_news_by_id(id, db)
        if r is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="News not found")
        return r
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Error getting news from database')


@app.delete("/{news_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_news_by_id_from_db(news_id: int, db: Session = Depends(get_db)):
    try:
        result = await delete_news_by_id(news_id, db)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="News not found")
        return result
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Error deleting news from database')
