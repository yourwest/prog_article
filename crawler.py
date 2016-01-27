import asyncio
import aiohttp
import re
import requests
import os


urls = ['http://www.colta.ru/authors/346',
        'http://www.colta.ru/authors/26',
        'http://www.colta.ru/authors/23']

MAIN_URL = 'http://www.colta.ru'


def collect_urls():
    article_urls = []
    for url in urls:
        page_content = requests.get(url).content.decode('utf8')
        article_url = re.findall(r'/articles/cinema/\d+', page_content, flags=re.DOTALL)
        author_number = re.search('/([0-9]+)\\b', url)
        if author_number is not None:
                author = author_number.group(1)
        for i in set(article_url):
            article_urls.append(MAIN_URL + i)
        article_info = (author, article_urls)
        try:
                os.mkdir(author)
        except:
                continue
    return article_info
    

@asyncio.coroutine
def get(*args, **kwargs):
    response = yield from aiohttp.request('GET', *args, **kwargs)
    return (yield from response.text())


def parse_html(page):
    # Полина часть
    # TODO: Вытащить текст, тему и просмотры. Вернуть кортеж (тема, просмотры, текст, автор)
    pass


@asyncio.coroutine
def downlaod_html(url, author):
    with (yield from sem):
        page = yield from get(url)
        print(url)
    articles = parse_html(page)

    # Гуля
    # TODO: Сохранить articles. Название файла - тема текста
    topic = articles[0]
    text =  articles[2]
    article = open('./' + author + '/' + topic + '.txt', 'w', encoding='utf-8')
    article.write(text)
    article.close()

# С помощью семафоров ограничиваем количество одновременных запросов (чтобы сайты не банили на пример)
sem = asyncio.Semaphore(1000)

# Создаем цикл, который будет производить загрузку url
loop = asyncio.get_event_loop()
f = asyncio.wait([downlaod_html(d) for d in collect_urls()])

# Ждем пока не загрузятся все нужные страницы
loop.run_until_complete(f)
