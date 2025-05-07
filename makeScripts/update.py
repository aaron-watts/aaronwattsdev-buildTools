#!/usr/bin/env python3

import sitemap, articles, feeds

if __name__ == "__main__":
    print('Updating sitemap.xml\n...')
    sitemap.main()
    print('Updating home and indexes\n...')
    articles.main()
    print('Updating RSS feeds\n...')
    feeds.main()
    print('Update complete')