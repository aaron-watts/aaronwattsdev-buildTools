import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from datetime import date

base_url = 'https://aaronwattsdev.com'
title_text = 'AaronWattsDev Projects'
description_text = 'Projects in coding, raspberry pi, linux and more'

# builds a basic xml element, populates text, and appends to specified parent
def build_element(el_parent, el_type, el_text=''):
    element = ET.SubElement(el_parent, el_type)
    if len(el_text):
        element.text = el_text
    return element

# builds a rss item from scraped project data
def build_item(title, link, description, project_date):
    link_text = f'{base_url}{link}'
    rss_item = build_element(rss_channel, 'item')
    build_element(rss_item, 'title', title)
    build_element(rss_item, 'link', link_text)
    build_element(rss_item, 'pubDate', project_date)
    build_element(rss_item, 'description', ' '.join(description.split()))
    build_element(rss_item, 'guid', link_text)
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

# Declare XML namespaces to be used
ET.register_namespace('', 'http://www.w3.org/2005/Atom')
ET.register_namespace('', 'http://search.yahoo.com/mrss/')

# create root rss element and set attributes
rss = ET.Element('rss')
rss.set('version', '2.0')
rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')
rss.set('xmlns:media', 'http://search.yahoo.com/mrss/')

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

# parse contents of home.html
with open('home.html') as f:
    txt = f.read()
    soup = BeautifulSoup(txt, 'lxml')

# create and populate an item element for each project
projects = soup.select('.project')
for project in projects:
    title = project.select_one('h2').text
    link = project.select_one('a')['href']
    description = project.select_one('.description').text
    html_date = project.select_one('time')
    project_date = date.fromisoformat(html_date['datetime'])
    fomratted_date = project_date.strftime('%a, %d %b %Y')
    build_item(title, link, description, fomratted_date)

# build and write the tree
tree = ET.ElementTree(rss)
ET.indent(tree)
tree.write('feed.xml', xml_declaration='version', encoding='UTF-8')
