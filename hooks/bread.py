"""Add breadcrumbs at the top of each page."""

import re

# Template for breadcrumb links
LINK = '  <a href="{0}">{1}</a>\n'

# Separator text between links
SEP = "  &nbsp;&gt;&nbsp;\n"

# Where to move tags (optional)
TAGS = "<!-- tags -->"

# Set of all linkable page URLs
URLS = set()


def on_files(files, config):
    """Called after the files collection is populated from the docs_dir."""
    for file in files:
        if file.src_uri.endswith(".md"):
            URLS.add(file.url)


def insert_link(bread, href, title, exists=True):
    """Insert the next link at the front of the breadcrumbs string."""
    if bread:
        bread = SEP + bread
    if exists:
        bread = LINK.format(href, title) + bread
    else:
        bread = title + bread
    return bread


def dirname(url):
    """Get the url of the parent directory."""
    idx = url[:-1].rfind("/")
    return url[:idx + 1] if idx != -1 else ""


def on_post_page(output, page, config):
    """Called after the template is rendered."""
    if not page.is_homepage:

        # Build the breadcrumb links (html code)
        bread = ""
        href = ".."
        url = dirname(page.url)
        for a in page.ancestors:
            # Special case: don't link index page
            if bread == "" and a.title == page.title:
                bread = a.title
                continue
            bread = insert_link(bread, href, a.title, url in URLS)
            # Update relative path and url
            href += "/.."
            url = dirname(url)

        # Append page's filename (if not index page)
        if page.title != page.parent.title:
            bread += SEP + "  " + page.url.split("/")[-2] + "\n"

        # Insert home page at the front
        bread = insert_link(bread, href, "Home")
        bread = f'\n<nav class="bread"><span>\n{bread}</span></nav>\n\n'

        # Place the breadcrumb above the page title
        pos = output.index("<h1")
        output = output[:pos] + bread + output[pos:]

        # Move tags (if present) to desired location
        pattern = r'<nav class="md-tags"(.*?)</nav>'
        match = re.search(pattern, output, re.DOTALL)
        if match:
            output = output[:match.start()] + output[match.end():]

            # Find and remove the tags comment
            pos = output.find(TAGS)
            if pos > -1:
                end = pos + len(TAGS)
                output = output[:pos] + output[end:]
            else:
                # Move tags into the breadcrumbs
                pos = output.index('<nav class="bread">')
                pos = output.index('</nav>', pos)

            # Change the tags <nav> to a <span>
            span = "<span" + match.group()[4:-4] + "span>"
            output = output[:pos] + span + output[pos:]

        return output
