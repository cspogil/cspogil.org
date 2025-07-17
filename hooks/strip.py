"""Remove HTML comments from Markdown source."""

import re


def on_page_markdown(markdown, page, config, files):
    """Called after the page's markdown is loaded from the source file."""
    return re.sub(r"<!--(.*?)-->", "", markdown, flags=re.DOTALL)
