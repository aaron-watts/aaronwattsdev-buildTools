import os
import xml.etree.ElementTree as ET

root_url = 'https://aaronwattsdev.com/'

def build_url(path=''):
    url = ET.SubElement(urlset, 'url')
    loc = ET.SubElement(url, 'loc')
    loc.text = f'{root_url}{path}'

ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
urlset = ET.Element('urlset')
urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')

build_url()
build_url('home/')

for filename in os.listdir('projects/'):
    build_url(f'{filename[:-5]}/')

tree = ET.ElementTree(urlset)
ET.indent(tree)
tree.write('sitemap.xml', xml_declaration='version', encoding='UTF-8')
