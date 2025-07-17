"""Add breadcrumbs at the top of each page."""

import re

# Template for breadcrumb links
LINK = '  <a href="{0}">{1}</a>\n'

# Separator text between links
SEP = "  &nbsp;&gt;&nbsp;\n"

# Where to move tags if present
TAGS = "<!-- tags -->"


def insert_link(bread, href, title):
    """Insert the next link at the front of the breadcrumbs string."""
    if bread:
        bread = SEP + bread
    if title.isdigit():
        bread = title + bread
    else:
        bread = LINK.format(href, title) + bread
    return bread


def on_post_page(output, page, config):
    """Called after the template is rendered."""
    if not page.is_homepage:

        # Build the breadcrumb links (html code)
        bread = ""
        href = ".."
        for a in page.ancestors:
            # Special case: don't link index page
            if bread == "" and a.title == page.title:
                bread = a.title
                continue
            bread = insert_link(bread, href, a.title)
            href += "/.."

        # Append page's filename unless index page
        if page.title != page.parent.title:
            bread += SEP + "  " + page.url.split("/")[-2] + "\n"

        # Insert home page at the front
        bread = insert_link(bread, href, "Home")
        bread = f'\n<nav class="bread">\n{bread}</nav>\n\n'

        # Place the breadcrumb above the page title
        pos = output.index("<h1")
        output = output[:pos] + bread + output[pos:]

        # Move tags (if present) below the page title
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
                pos = output.index("</h1>") + 6

            # Change the tags <nav> to a <span>
            span = "<span" + match.group()[4:-4] + "span>"
            output = output[:pos] + span + output[pos:]

        return output
