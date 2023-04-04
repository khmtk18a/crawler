import requests
import re
import redis
from hashlib import md5
from bs4 import BeautifulSoup
from celery import Celery
from celery.exceptions import Reject
from typing import TypedDict

app = Celery('crawler', broker='pyamqp://guest@rabbitmq//',
             backend='redis://redis')

rd = redis.Redis(host='redis')
regex = r'^https:\/\/www\.nhaccuatui\.com\/bai-hat\/[\w-]+\.([\w\d]+)\.html$'


class Song(TypedDict):
    id: str
    name: str
    artist: str
    url: str


@app.task(acks_late=True)
def dfs_crawler(url: str, depth: int) -> Song:
    lock = rd.lock(md5(url.encode()).hexdigest(), blocking=False)
    if not lock.acquire():
        raise Reject('URL has been indexed')

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    if depth > 0:
        for link in soup.findAll('a'):
            href: str = link.get('href')
            if re.match(regex, href):
                dfs_crawler.delay(href, depth-1)

    try:
        song_name = soup.find(
            'h1', {'itemprop': 'name'}).text.strip()  # type: ignore
        artist_name = soup.find(
            'h2', {'class': 'name-singer'}).text.strip()  # type: ignore
    except:
        raise RuntimeError('Information extraction failed')

    return Song(
        id=md5(song_name.encode()).hexdigest(),
        name=song_name,
        artist=artist_name,
        url=url
    )
