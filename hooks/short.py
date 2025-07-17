"""Various shortcuts and find-and-replace patterns."""

import bibtexparser
import io
import os
import re
import sys


SUBS = [
    (r"{EngageCSEdu}", "[EngageCSEdu](https://www.engage-csedu.org/)"),
    (r"<!-- DO NOT EDIT (.*?)-->", ""),
]


def on_page_markdown(markdown, page, config, files):
    """Called after the page's markdown is loaded from the source file."""

    # Replace all shortcuts
    for pattern, replace in SUBS:
        markdown = re.sub(pattern, replace, markdown, flags=re.DOTALL)

    # Append activity metadata
    if page.url.startswith("activities"):
        md_path = "docs/" + page.file.src_uri
        bib_path = md_path[:-2] + "bib"
        if os.path.exists(bib_path):

            # Parse the bib file
            library = bibtexparser.parse_file(bib_path)
            n = len(library.failed_blocks)
            if n > 0:
                print(f"Error: {n} blocks failed to parse")
                sys.exit(1)
            n = len(library.entries)
            if n != 1:
                print(f"Error: Found {n} entries (should be 1)")
                sys.exit(1)

            # Generate the Markdown
            out = io.StringIO()
            out.write("\n## Metadata\n\n")
            name = os.path.basename(bib_path)
            down = '{download="' + name + '"}'
            out.write(f"[:material-download: Download .bib file]({name}){down}\n\n")
            out.write("Field | Value\n------|------\n")
            entry = library.entries[0]
            for fkey, field in entry.fields_dict.items():
                out.write(f"{fkey} | ")
                if fkey != "url":
                    out.write(f"{field.value}\n")
                else:
                    # Abbreviate the URL to allow text wrapping
                    url = field.value
                    pos = url.index("/", 8)
                    abbr = url[:pos+1] + "..."
                    out.write(f"[{abbr}]({url})\n")

            # Append at the bottom
            markdown += out.getvalue()

    return markdown
