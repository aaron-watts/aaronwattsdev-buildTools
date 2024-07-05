from bs4 import BeautifulSoup
import os
from datetime import date

projects = []

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
    keywords = project_soup.select_one('meta[name=keywords]')['content'].split(',')
    keywords = [kw.lstrip() for kw in keywords]
    
    projects.append({
        'title' : title,
        'description' : description,
        'keywords' : keywords,
        'date' : project_date,
        'datehtml' : html_date,
        'link': f'/{path_name[:-5]}'
    })

def date_sort(e):
    return e['date']

projects.sort(reverse=True, key=date_sort)

with open('home.html') as inf:
    txt = inf.read()
    soup = BeautifulSoup(txt, 'lxml')

main_element = soup.select_one('main')
main_element.clear()

for project in projects:
    project_div = soup.new_tag('div')
    project_div['class'] = 'project'
    project_header = soup.new_tag('h2')
    project_header.string = project['title']
    project_div.append(project_header)
    project_date = soup.new_tag('time', datetime=project['datehtml']['datetime'])
    project_date.string = project['datehtml'].text
    project_div.append(project_date)
    project_ul = soup.new_tag('ul')
    project_ul['class'] = 'topic-container'
    for topic in project['keywords']:
        topic_li = soup.new_tag('li')
        topic_li['class'] = 'topic'
        topic_li.string = topic
        project_ul.append(topic_li)
    project_div.append(project_ul)
    project_link = soup.new_tag('a', href=project['link'])
    project_link.string = 'Go to project'
    project_div.append(project_link)
    project_description = soup.new_tag('p')
    project_description['class'] = 'description'
    project_description.string = project['description']
    project_div.append(project_description)
    main_element.append(project_div)

with open ('home.html', 'w') as outf:
    outf.write(BeautifulSoup.prettify(soup))