import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import os
from datetime import date

base_url = 'https://aaronwattsdev.com'
title_text = 'AaronWattsDev Projects'
description_text = 'Projects in coding, raspberry pi, linux and more'
projects = []

# builds a basic xml element, populates text, and appends to specified parent
def build_element(el_parent, el_type, el_text=''):
    element = ET.SubElement(el_parent, el_type)
    if len(el_text):
        element.text = el_text
    return element

# builds a rss item from scraped project data
def build_item(title, link, description, project_date, content):
    link_text = f'{base_url}{link}'
    rss_item = build_element(rss_channel, 'item')
    build_element(rss_item, 'title', title)
    build_element(rss_item, 'link', link_text)
    build_element(rss_item, 'pubDate', project_date)
    build_element(rss_item, 'description', ' '.join(description.split()))
    build_element(rss_item, 'guid', link_text)
    build_element(
        rss_item,
        'content:encoded',
        str(content)
        .strip()
        .replace('\\n', '')
        .replace('="/', '="https://aaronwattsdev.com/')
    )
    build_media(rss_item, link)

# called by build_item: builds complex media elements and appends to item parent
def build_media(el_parent, el_link):
    img_link = f'{base_url}/images{el_link}.jpg'
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

# format main content by including line breaks within pre elements
def format_main_content(content):
    content_str = ''
    for child in content.children:
        if child.name == 'pre':
            content_str += str(child)
        else:
            content_str += ' '.join(str(child).split())
    return content_str

for f in os.scandir('projects'):
    path_name = f'projects/{f.name}'
    with open(path_name) as projectf:
        project_txt = projectf.read()
        project_soup = BeautifulSoup(project_txt, 'lxml')
    title = project_soup.select_one('h1').text
    intro = project_soup.select_one('p#intro').text
    description = ' '.join(intro.split())
    html_date = project_soup.select_one('time')
    project_date = date.fromisoformat(html_date['datetime'])
    formatted_date = project_date.strftime('%a, %d %b %Y')
    keywords = project_soup.select_one('meta[name=keywords]')['content'].split(',')
    keywords = [kw.lstrip() for kw in keywords]
    main_element = project_soup.select_one('main')
    content = format_main_content(main_element)
    
    projects.append({
        'title' : title,
        'description' : description,
        'keywords' : keywords,
        'date' : project_date,
        'formatted_date' : formatted_date,
        'link': f'/{path_name[:-5]}',
        'content': content
    })

def date_sort(e):
    return e['date']

projects.sort(reverse=True, key=date_sort)

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
atom_link.set('href', f'{base_url}/feed.xml')
atom_link.set('rel', 'self')
atom_link.set('type', 'applications/rss+xml')
build_element(rss_channel, 'title', title_text)
build_element(rss_channel, 'link', f'{base_url}/home')
build_element(rss_channel, 'description', description_text)
build_element(rss_channel, 'category', 'Technology')

# create and populate an item element for each project
for project in projects:
    build_item(
        project['title'],
        project['link'],
        project['description'],
        project['formatted_date'],
        project['content']
    )

# build and write the tree
tree = ET.ElementTree(rss)
ET.indent(tree)
tree.write('feed.xml', xml_declaration='version', encoding='UTF-8')