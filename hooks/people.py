"""Add links to People pages by searching for names."""

import re
import yaml

# Map names to urls
PEOPLE = {}


def on_files(files, config):
    """Called after the files collection is populated from the docs_dir."""
    for file in files:
        if file.src_uri.startswith("people/"):

            # Get the front matter block
            block = ""
            with open("docs/" + file.src_uri) as f:
                line = f.readline()
                if not line.startswith("---"):
                    continue  # Next file
                while not (line := f.readline()).startswith("---"):
                    block += line

            # Add each name to the dict
            data = yaml.safe_load(block)
            for name in data["names"]:
                PEOPLE[name] = file.src_uri


def on_page_markdown(markdown, page, config, files):
    """Called after the page's markdown is loaded from the source file."""

    if page.url.startswith("people"):

        # TODO List activities and publications
        return markdown

    else:

        # Get the text after the heading
        pattern = r"^\s*# (.+)$"
        match = re.search(pattern, markdown, re.MULTILINE)
        neck = match.end() if match else 0
        head = markdown[:neck]
        body = markdown[neck:]

        # Determine the relative path
        count = page.url.count("/")
        if not page.is_index:
            count -= 1
        path = "../" * count

        # Link every name in the body text
        for name, url in PEOPLE.items():
            repl = f"[{name}]({path}{url})"
            body = re.sub(name, repl, body)
        return head + body
