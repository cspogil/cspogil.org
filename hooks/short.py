"""Find and replace short patterns."""

import re

SUBS = [
    (r"{EngageCSEdu}", "[EngageCSEdu](https://www.engage-csedu.org/)"),
    (r"{The POGIL Project}", "[The POGIL Project](https://www.pogil.org/)"),
    (r"<!-- DO NOT EDIT (.*?)-->", ""),
]


def on_page_markdown(markdown, page, config, files):
    """Called after the page's markdown is loaded from the source file."""

    # Insert file snippets now so they're included below
    pattern = r'^--8<--\s+"([^"]+)"$'
    match = re.search(pattern, markdown, re.MULTILINE)
    if match:
        with open(match.group(1)) as file:
            snippet = file.read()
        beg, end = match.span()
        markdown = markdown[:beg] + snippet + markdown[end:]

    # Replace all shortcuts
    for pattern, replace in SUBS:
        markdown = re.sub(pattern, replace, markdown, flags=re.DOTALL)

    return markdown
