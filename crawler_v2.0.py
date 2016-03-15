import re
import requests
import os

urls = ['http://www.colta.ru/authors/471',
        'http://www.colta.ru/authors/66',
        'http://www.colta.ru/authors/26']

MAIN_URL = 'http://www.colta.ru'


def collect_urls(url):
    article_urls = []
    page_content = requests.get(url).content.decode('utf8')
    article_url = re.findall(r'/articles/\w+/\d+', page_content, flags=re.DOTALL)
    for i in set(article_url):
        article_urls.append(MAIN_URL + i)
    next_page = re.search(r'/authors/\d+\?page=\d+', page_content, flags=re.DOTALL)
    if next_page is not None:
            next_page_url = MAIN_URL + next_page.group(0)
            for item in collect_urls(next_page_url):
                article_urls.append(item)
    return article_urls


def parse_html(page):
    article_name = re.findall('<section class="article.*?<h1>(.*?)</h1>', page, flags=re.DOTALL)
    article_authors = re.findall('<a href="/authors/(\\d+)">(.*?)</a>', page, flags=re.DOTALL)
    article_views = re.findall('<span class="view">(\\d+)</span>', page, flags=re.DOTALL)
    article_content = re.findall('<div class="content">(.*?)<div class="share">', page, flags=re.DOTALL)
    if article_content == []:
        article_content = re.findall('<article class="content bigmat_content">.*?<p>(.*?)</article', page, flags=re.DOTALL)
    if article_name != []:    
        name = ''.join(article_name[0].replace('\n', '').replace('/', '-').strip(' '))
        views = article_views[0]
        content = re.sub('<.*?>', '', article_content[0])
        return [name, views, content, article_authors]


for url in urls:
    author_number = re.search('/([0-9]+)\\b', url)
    author = author_number.group(1)
    try:
        os.mkdir(author)
    except:
        continue

    article_urls = collect_urls(url)
    for article_url in article_urls:
        article_page = requests.get(article_url).content.decode('utf8')
        info = parse_html(article_page)
        if info is not None:
            if info[0].endswith('»'):
                continue
            if len(info[2].split()) < 500:
                continue
            else:
                article = open('./' + author + '/' + info[0] + '.txt', 'w', encoding='utf-8')
                article.write(info[2])
                article.close()
