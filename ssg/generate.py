# Generates the static site into "/static" using the "/articles"

import markdown
import os

print(os.getcwd())

rootdir = os.path.join(os.getcwd(), 'articles')

for directory in os.listdir(rootdir):
    # look for content.md
    path = os.path.join(rootdir, directory)
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
        
    html = markdown.markdown(content)

    print(html)
    