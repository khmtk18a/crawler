import requests
import json
import sys
import os
from bs4 import BeautifulSoup
from ictu import connection


def get_links(url):
    links = []
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        for link in soup.find_all('a', href=True):
            links.append(link['href'])
        return links
    except:
        return links


def encode(url: str, depth: int) -> str:
    return json.dumps({'url': url, 'depth': depth})


def dfs_crawler(start_url, max_depth):
    channel = connection.channel()
    channel.queue_declare(queue='crawler')
    channel.basic_publish(
        exchange='',
        routing_key='crawler',
        body=encode(start_url, 0)
    )

    visited = set()

    def callback(ch, method, properties, body: str):
        data = json.loads(body)
        url, depth = data['url'], data['depth']
        if url not in visited and depth <= max_depth:
            visited.add(url)
            print(f"Visiting {url}")
            links = get_links(url)
            for link in links:
                channel.basic_publish(
                    exchange='',
                    routing_key='crawler',
                    body=encode(link, depth+1)
                )

    channel.basic_consume(
        queue='crawler', on_message_callback=callback, auto_ack=True)

    print('[*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        dfs_crawler('https://vi.wikipedia.org', 1)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
