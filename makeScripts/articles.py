from bs4 import BeautifulSoup
import os
from datetime import date
from utils import *

def main():
    articles = {
        'all': []
    }

    for directory in sub_directories:
        articles[directory] = []
        for f in os.scandir(directory):
            if f.name != "index.html" and not f.name.endswith('.xml'):
                path_name = f'{directory}/{f.name}'
                with open(path_name) as articlef:
                    article_txt = articlef.read()
                    article_soup = BeautifulSoup(article_txt, 'lxml')
                title = article_soup.select_one('h1').text
                intro = article_soup.select_one('p#intro').text
                description = ' '.join(intro.split())
                html_date = article_soup.select_one('time')
                article_date = date.fromisoformat(html_date['datetime'])
                keywords = article_soup.select_one('meta[name=keywords]')['content'].split(',')
                keywords = [kw.lstrip() for kw in keywords]
                
                articles[directory].append({
                    'title' : title,
                    'description' : description,
                    'keywords' : keywords,
                    'date' : article_date,
                    'datehtml' : html_date,
                    'link': f'/{path_name[:-5]}'
                })

        articles['all'].extend(articles[directory])

    for category in articles:
        articles[category].sort(reverse=True, key=date_sort)

    for directory in sub_directories:
        with open(f'{directory}/index.html') as inf:
            txt = inf.read()
            soup = BeautifulSoup(txt, 'lxml')

        main_element = soup.select_one('main')
        main_element.clear()

        for article in articles[directory]:
            article_div = soup.new_tag('div')
            article_div['class'] = 'article'
            article_header = soup.new_tag('h2')
            article_header.string = article['title']
            article_div.append(article_header)
            article_date = soup.new_tag('time', datetime=article['datehtml']['datetime'])
            article_date.string = article['datehtml'].text
            article_div.append(article_date)
            article_ul = soup.new_tag('ul')
            article_ul['class'] = 'topic-container'
            for topic in article['keywords']:
                topic_li = soup.new_tag('li')
                topic_li['class'] = 'topic'
                topic_li.string = topic
                article_ul.append(topic_li)
            article_div.append(article_ul)
            article_link = soup.new_tag('a', href=article['link'])
            article_link.string = 'Go to article'
            article_div.append(article_link)
            article_description = soup.new_tag('p')
            article_description['class'] = 'description'
            article_description.string = article['description']
            article_div.append(article_description)
            main_element.append(article_div)

        with open (f'{directory}/index.html', 'w') as outf:
            outf.write(str(soup))

    articles['all'].sort(reverse=True, key=date_sort)
    latest_article = articles['all'][0]

    with open('home.html') as inf:
        txt = inf.read()
        soup = BeautifulSoup(txt, 'lxml')

    latest = soup.select_one('.article')
    latest.clear()

    latest_header = soup.new_tag('h3')
    latest_header.string = latest_article['title']
    latest.append(latest_header)
    latest_date = soup.new_tag('time', datetime=latest_article['datehtml']['datetime'])
    latest_date.string = latest_article['datehtml'].text
    latest.append(latest_date)
    latest_ul = soup.new_tag('ul')
    latest_ul['class'] = 'topic-container'
    for topic in latest_article['keywords']:
        topic_li = soup.new_tag('li')
        topic_li['class'] = 'topic'
        topic_li.string = topic
        latest_ul.append(topic_li)
    latest.append(latest_ul)
    latest_link = soup.new_tag('a', href=latest_article['link'])
    latest_link.string = 'Go to article'
    latest.append(latest_link)
    latest_description = soup.new_tag('p')
    latest_description['class'] = 'description'
    latest_description.string = latest_article['description']
    latest.append(latest_description)

    with open('home.html', 'w') as outf:
        outf.write(str(soup))

if __name__ == "__main__":
    main()
