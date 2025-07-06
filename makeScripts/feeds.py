import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import os
from datetime import date
from utils import date_sort, sub_directories, root_url, format_main_content

def main():
    # builds a basic xml element, populates text, and appends to specified parent
    def build_element(el_parent, el_type, el_text=''):
        element = ET.SubElement(el_parent, el_type)
        if len(el_text):
            element.text = el_text
        return element

    # builds a rss item from scraped article data
    def build_item(article, rss_channel):        
        link_text = f'{root_url}{article["link"]}'
        rss_item = build_element(rss_channel, 'item')
        build_element(rss_item, 'title', article['title'])
        build_element(rss_item, 'link', link_text)
        build_element(rss_item, 'pubDate', article['formatted_date'])
        build_element(rss_item, 'description', ' '.join(article['description'].split()))
        build_element(rss_item, 'guid', link_text)
        build_element(
            rss_item,
            'content:encoded',
            str(article['content'])
            .strip()
            .replace('\\n', '')
            .replace('="/', '="https://aaronwatts.dev/')
        )
        build_media(rss_item, article['link'])

    # called by build_item: builds complex media elements and appends to item parent
    def build_media(el_parent, el_link):
        img_link = f'{root_url}/images{el_link}.jpg'
        enclosure = ET.SubElement(el_parent, 'enclosure')
        enclosure.set('url', img_link)
        enclosure.set('length', '0')
        enclosure.set('type','image/jpeg')
        media_thumbnail = ET.SubElement(el_parent, 'media:thumbnail')
        media_thumbnail.set('url', img_link)
        media_thumbnail.set('width', '1920')
        media_thumbnail.set('height', '1080')
        media_content = ET.SubElement(el_parent, 'media:content')
        media_content.set('type', 'image/jpeg')
        media_content.set('url', img_link)

    def build_feed(sub_dir=False):
        feed_url = f'{root_url}' if not sub_dir else f'{root_url}/{sub_dir}'
        page_url = f'{root_url}/home' if not sub_dir else f'{root_url}/{sub_dir}'
        feed_path = 'feed.xml' if not sub_dir else f'{sub_dir}/feed.xml'
        directory = 'all' if not sub_dir else sub_dir
        title = feed_data['all']['title'] if not sub_dir else feed_data[sub_dir]['title']
        description = feed_data['all']['description'] if not sub_dir else feed_data[sub_dir]['description']

        # Declare XML namespaces to be used
        ET.register_namespace('', 'http://www.w3.org/2005/Atom')
        ET.register_namespace('', 'http://search.yahoo.com/mrss/')
        ET.register_namespace('', 'http://purl.org/rss/1.0/modules/content/')

        # create root rss element and set attributes
        rss = ET.Element('rss')
        rss.set('version', '2.0')
        rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')
        rss.set('xmlns:media', 'http://search.yahoo.com/mrss/')
        rss.set('xmlns:content', 'http://purl.org/rss/1.0/modules/content/')

        # add necessary child elements to root element and set attributes if required
        rss_channel = build_element(rss, 'channel')
        atom_link = ET.SubElement(rss_channel, 'atom:link')
        atom_link.set('href', f'{feed_url}/feed.xml')
        atom_link.set('rel', 'self')
        atom_link.set('type', 'applications/rss+xml')
        build_element(rss_channel, 'title', title)
        build_element(rss_channel, 'link', f'{page_url}')
        build_element(rss_channel, 'description', description)
        build_element(rss_channel, 'category', 'Technology')

        # create and populate an item element for each project
        for article in articles[directory]:
            build_item(article, rss_channel)
        
        # build and write the tree
        tree = ET.ElementTree(rss)
        ET.indent(tree)
        tree.write(feed_path, xml_declaration='version', encoding='UTF-8')

    feed_data = {
        'all': {
            'title': 'AaronWattsDev Latest',
            'description': 'The most recent content on AaronWattsDev'
        },
        'guides': {
            'title': 'AaronWattsDev Guides',
            'description': 'Guides for coding, raspberry pi, linux and more'
        },
        'tech': {
            'title': 'AaronWattsDev Tech',
            'description': 'Thoughtful tech that offers something different'
        }
    }
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
                formatted_date = article_date.strftime('%a, %d %b %Y')
                keywords = article_soup.select_one('meta[name=keywords]')['content'].split(',')
                keywords = [kw.lstrip() for kw in keywords]
                main_element = article_soup.select_one('main')
                content = format_main_content(main_element)
                
                articles[directory].append({
                    'title' : title,
                    'description' : description,
                    'keywords' : keywords,
                    'date' : article_date,
                    'formatted_date' : formatted_date + ' 08:00:00 GMT',
                    'link': f'/{path_name[:-5]}',
                    'content': content
                })

        articles[directory].sort(reverse=True, key=date_sort)
        articles['all'] = articles['all'] + articles[directory]

        build_feed(directory)

    articles['all'].sort(reverse=True, key=date_sort)

    build_feed()

if __name__ == "__main__":
    main()
