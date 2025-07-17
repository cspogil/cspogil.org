"""Add breadcrumbs at the top of each page."""

import re

# Template for breadcrumb links
LINK = '  <a href="{0}">{1}</a>\n'

# Separator text between links
SEP = "  &nbsp;&gt;&nbsp;\n"


def insert_link(bread, href, title):
    """Insert the next link at the front of the breadcrumbs string."""
    if bread:
        bread = SEP + bread
    if title.isdigit():
        bread = title + bread
    else:
        bread = LINK.format(href, title) + bread
    return bread


def on_page_markdown(markdown, page, config, files):
    """Called after the page's markdown is loaded from the source file."""
    if not page.is_homepage:

        # Build the breadcrumb
        bread = ""
        href = ".."
        for a in page.ancestors:
            # Special case: don't link index page
            if bread == "" and a.title == page.title:
                bread = a.title
                continue
            bread = insert_link(bread, href, a.title)
            href += "/.."

        # Append page's filename (unless index page)
        if page.title != page.parent.title:
            bread += SEP + "  " + page.url.split("/")[-2] + "\n"

        # Insert home page at the front
        bread = insert_link(bread, href, "Home")
        bread = f'<nav class="bread">\n{bread}</nav>\n\n'

        # Place the breadcrumb after the metadata
        pattern = r"^---\s*\n(.*?)\n---\s*"
        match = re.search(pattern, markdown, re.DOTALL)
        pos = match.end() if match else 0
        return markdown[:pos] + bread + markdown[pos:]
