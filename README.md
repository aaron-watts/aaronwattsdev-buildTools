# aaronwattsdev-buildTools

These are the build tools I use for [aaronwattsdev.com](https://aaronwattsdev.com). They are specific to my own website and it is not reccomended to use the scripts '_as is_' in other projects.

## Page Templates

### Project page template

A template for the blog-style project pages. Site is written in pure HTML, CSS and JavaScript, no templating engine is used. This template is simply to ensure all pages conform to the same structure to promote unity between pages and allow the build scripts to work correctly.

## Make Scripts

### sitemap.py

Generates the `sitemap.xml` file. Crawls through directory and builds XML file based on HTML files it finds.

### rss.py

Generates the `feed.xml` file. Uses the projects list page, currently `home.html` to generate an XML RSS feed. Should be run ___after___ `projects.py`. The images directory structure and relevant filenames are expected to match the projects directory and filenames, for example, the first picture located within `projects/project-1.html` should be located at `images/projects/project-1.jpg`.

### projects.py

Crawls the projects directory, and scrapes the relevant data to build projects within the projects list page, currently `home.html`. It only writes over whatever is in the `main` element, and does not affect the rest of the document, meaning you can make changes elsewhere in the document and they will persist at each rewrite. It will retrieve a title, published date, the intro paragraph, and the meta keywords list, and use these to generate a div for each project. It tracks the filepath to generate links to relevant pages, and uses the meta keywords to generate a list of topics, that can be used via an in page script to filter the projects list by selected topic. Beautiful Soup's prettify method creates additional whitespace, so `string.trim()` has to be used in the page script to correct for this.