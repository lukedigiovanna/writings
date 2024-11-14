# Generates the static site into "/static" using the "/articles"

import markdown
import os
import shutil
import yaml

print(os.getcwd())

base_url = "writings"
writings_url = "articles"

articles_dir = os.path.join(os.getcwd(), 'articles')
template_dir = os.path.join(os.getcwd(), 'template')

site_dir = os.path.join(os.getcwd(), 'site')
writings_dir = os.path.join(site_dir, writings_url)

template_dir = os.path.join(os.getcwd(), 'template')


def read_template(name):
    with open(os.path.join(template_dir, name), "r") as f:
        return f.read().replace("{base_url}", base_url)

article_template = read_template("article.html")
home_template = read_template("home.html")
tags_template = read_template("tags.html")
archive_template = read_template("archive.html")

# make/clear site folder
if os.path.exists(site_dir):
    shutil.rmtree(site_dir)
os.makedirs(site_dir)
os.makedirs(writings_dir)
# Loop over all files in the source folder
for filename in os.listdir(template_dir):
    file_path = os.path.join(template_dir, filename)
    # Check if it's a file (not a folder) and not an HTML file
    if os.path.isfile(file_path) and not filename.lower().endswith(('.html', '.htm')):
        shutil.copy(file_path, site_dir)
        print(f"Copied: {filename}")

articles = [] # article is a tuple with title and date
all_tags = set()

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
        
    content_html = markdown.markdown(content, extensions=['fenced_code'])
    metadata_yaml = yaml.safe_load(metadata)

    title = metadata_yaml["title"]
    date = metadata_yaml["date"]
    tags = metadata_yaml["tags"]

    for t in tags:
        all_tags.add(t)

    # Replace article with proper content
    html = article_template.replace("{title}", title) \
                           .replace("{date}", date) \
                           .replace("{content}", content_html)

    # make a directory in the site with the same content
    site_article_dir = os.path.join(writings_dir, directory)
    os.makedirs(site_article_dir)
    with open(os.path.join(site_article_dir, "index.html"), "w") as f:
        f.write(html)

    articles.append((directory, title, date, tags, content))

# Generates the HTML for the article link
def make_article_link(article):
    directory, title, date, tags, content = article
    return f'<div class="article-block"> \
                <a href="{base_url}/{writings_url}/{directory}"> \
                    <div class="article-block-content"> \
                        <h1> {title} </h1> \
                        <h4> {date} </h4> \
                        <p> {content[:300]} </p> \
                    </div> \
                </a> \
            </div>'

def make_articles_list(articles):
    content = "<ul>"
    for article in articles:
        content += make_article_link(article)
    content += "</ul>"
    return content

def make_tag_link(tag):
    return f'<a href="/" class="tag-button">{tag}</a>'

def make_tags_list(tags):
    content = ""
    for tag in tags:
        content += make_tag_link(tag)
    return content

def write_index_html(path, content):
    full_path = os.path.join(site_dir, path)
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    with open(os.path.join(full_path, "index.html"), "w") as f:
        f.write(content)

index_html = home_template.replace("{article_list}", make_articles_list(articles))
archive_html = archive_template
tags_html = tags_template.replace("{tags}", make_tags_list(all_tags))

write_index_html("./", index_html)
write_index_html("./archive", archive_html)
write_index_html("./tags", tags_html)
