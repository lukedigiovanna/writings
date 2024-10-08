# Generates the static site into "/static" using the "/articles"

import markdown
import os
import shutil
import yaml

print(os.getcwd())

articles_dir = os.path.join(os.getcwd(), 'articles')
template_dir = os.path.join(os.getcwd(), 'template')

site_dir = os.path.join(os.getcwd(), 'site')
template_dir = os.path.join(os.getcwd(), 'template')

with open(os.path.join(template_dir, "article.html"), "r") as f:
    article_template = f.read()
with open(os.path.join(template_dir, "home.html"), "r") as f:
    home_template = f.read()

# make/clear site folder
if os.path.exists(site_dir):
    shutil.rmtree(site_dir)
os.makedirs(site_dir)
shutil.copy(os.path.join(template_dir, "index.css"), os.path.join(site_dir, "index.css"))

articles = [] # article is a tuple with title and date

for directory in os.listdir(articles_dir):
    # look for content.md
    path = os.path.join(articles_dir, directory)
    content_path = os.path.join(path, 'content.md')
    metadata_path = os.path.join(path, 'metadata.yaml')
    if not os.path.exists(content_path):
        raise Exception("No content.md file found for directory " + directory)
    if not os.path.exists(metadata_path):
        raise Exception("No metadata.yaml file found for directory " + directory)

    # Read the content and metadata
    with open(content_path, "r") as f:
        content = f.read()
    with open(metadata_path, "r") as f:
        metadata = f.read()
        
    content_html = markdown.markdown(content)
    metadata_yaml = yaml.safe_load(metadata)

    title = metadata_yaml["title"]
    date = metadata_yaml["date"]

    # Replace article with proper content
    html = article_template.replace("{title}", title) \
                           .replace("{date}", date) \
                           .replace("{content}", content_html)

    # make a directory in the site with the same content
    site_article_dir = os.path.join(site_dir, directory)
    os.makedirs(site_article_dir)
    with open(os.path.join(site_article_dir, "index.html"), "w") as f:
        f.write(html)

    articles.append((directory, metadata_yaml["title"], metadata_yaml["date"]))

# Generates the HTML for the article link
def make_article_link(article):
    return f'<li><a href="{directory}">{article[1]}</a></li>'

def make_articles_list(articles):
    content = "<ul>"
    for article in articles:
        content += make_article_link(article)
    content += "</ul>"
    return content

index_html = home_template.replace("{article_list}", make_articles_list(articles))

with open(os.path.join(site_dir, "index.html"), "w") as f:
    f.write(index_html)