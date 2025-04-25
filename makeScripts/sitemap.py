import os
import xml.etree.ElementTree as ET

root_url = 'https://aaronwatts.dev/'
sub_directories = [
    'guides/',
    'tech/'
]

def build_url(path=''):
    url = ET.SubElement(urlset, 'url')
    loc = ET.SubElement(url, 'loc')
    loc.text = f'{root_url}{path}'

ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
urlset = ET.Element('urlset')
urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')

build_url()
build_url('home/')

for directory in sub_directories:
    build_url(directory)
    for filename in os.listdir(directory):
        url = filename[:-5]
        if (url != "index" and not filename.endswith('.xml')):
            build_url(f'{directory}{url}/')

tree = ET.ElementTree(urlset)
ET.indent(tree)
tree.write('sitemap.xml', xml_declaration='version', encoding='UTF-8')
