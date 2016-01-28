import asyncio
import aiohttp
import re
import requests


urls = ['http://www.colta.ru/authors/346',
        'http://www.colta.ru/authors/26',
        'http://www.colta.ru/authors/23']

MAIN_URL = 'http://www.colta.ru'


def collect_urls():
    article_urls = []
    for url in urls:
        page_content = requests.get(url).content.decode('utf8')
        article_url = re.findall(r'/articles/cinema/\d+', page_content, flags=re.DOTALL)
        for i in set(article_url):
            article_urls.append(MAIN_URL + i)
    return article_urls
    

@asyncio.coroutine
def get(*args, **kwargs):
    response = yield from aiohttp.request('GET', *args, **kwargs)
    return (yield from response.text())


def parse_html(page):
    article_name = re.findall('<section class="article.*?<h1>(.*?)</h1>', page, flags=re.DOTALL)
    article_authors = re.findall('<a href="/authors/(\\d+)">(.*?)</a>', page, flags=re.DOTALL)
    article_views = re.findall('<span class="view">(\\d+)</span>', page, flags=re.DOTALL)
    article_content = re.findall('<div class="content">(.*?)<div class="share">', page, flags=re.DOTALL)
    if article_content == []:
        article_content = re.findall('<article class="content bigmat_content">.*?<p>(.*?)</article', page, flags=re.DOTALL)
    name = ''.join(article_name[0].replace('\n', '').strip(' '))
    views = article_views[0]
    content = re.sub('<.*?>', '', article_content[0])
    return (name, views, content, article_authors)



@asyncio.coroutine
def downlaod_html(url):
    with (yield from sem):
        page = yield from get(url)
        print(url)
    article_data = parse_html(page)
    print('./' + article_data[3][0][0][0] + '/' + article_data[0])
    article = open('./' + article_data[0] + '.txt', 'w', encoding='utf-8')
    article.write(article_data[2])
    article.close()

# С помощью семафоров ограничиваем количество одновременных запросов (чтобы сайты не банили на пример)
sem = asyncio.Semaphore(1000)

# Создаем цикл, который будет производить загрузку url
loop = asyncio.get_event_loop()
f = asyncio.wait([downlaod_html(d) for d in collect_urls()])

# Ждем пока не загрузятся все нужные страницы
loop.run_until_complete(f)
