root_url = 'https://aaronwatts.dev'

sub_directories = [
    'guides',
    'tech'
]

def date_sort(e):
    return e['date']

# format main content by including line breaks within pre elements
def format_main_content(content):
    content_str = ''
    for child in content.children:
        if child.name == 'pre':
            content_str += str(child)
        else:
            content_str += ' '.join(str(child).split())
    return content_str