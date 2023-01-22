import requests
from bs4 import BeautifulSoup
import multiprocessing

URL = ['https://www.kinofilms.ua/ukr/news/',
       'https://football24.ua/',
       'https://www.pravda.com.ua/news/'
       ]


def get_movie_news(url=URL[0]):
    movie_news = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'html.parser')
    data = soup.find_all('article', class_='block')
    for item in data:
        movie_item = {}
        # movie_item['created'] = item.find('div', class_='block-meta').text.strip()
        created = item.find('div', class_='block-meta').text.strip().split('\xa0')
        time = created[4][:5]
        created_date = ' '.join(created[0:2] + [time])
        movie_item['created'] = created_date
        movie_item['title'] = item.find('div', class_='h1').text.strip()
        link = item.find('a').get('href')
        movie_item['link'] = 'https://www.kinofilms.ua' + link
        movie_item['category'] = 'Кіно'
        movie_news.append(movie_item)
        print(movie_item)
    return movie_news


def get_football_news(url=URL[1]):
    football_news = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'html.parser')
    data = soup.find_all('li', class_='news-list-item important')
    for item in data:
        foot_news = {}
        foot_news['created'] = item.find('div', class_='time').text.strip()
        foot_news['title'] = item.find('div', class_='title').text.strip()
        foot_news['link'] = item.find('a').get('href')
        foot_news['category'] = 'Футбол'
        football_news.append(foot_news)
        print(foot_news)
    return football_news


def get_news(url=URL[2]):
    news = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'html.parser')
    data = soup.find_all('div', class_='article_news_list article_news_bold')
    for item in data:
        news_item = {}
        news_item['created'] = item.find('div', class_='article_time').text.strip()
        news_item['title'] = item.find('div', class_='article_header').text.strip()
        link = item.find('a').get('href')
        if 'https://www.epravda.com.ua' in link:
            news_item['link'] = link
        else:
            news_item['link'] = 'https://www.pravda.com.ua' + link
        news_item['category'] = 'Новини'
        news.append(news_item)
        print(news_item)
    return news


def get_all_news():
    with multiprocessing.Pool(3) as process:
        movie_news = process.apply_async(get_movie_news)
        football_news = process.apply_async(get_football_news)
        news = process.apply_async(get_news)
        return movie_news.get() + football_news.get() + news.get()
