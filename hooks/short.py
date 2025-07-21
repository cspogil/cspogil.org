"""Find and replace short patterns and render BibTeX entries."""

import bibtexparser
import io
import os
import re


SUBS = [
    (r"{EngageCSEdu}", "[EngageCSEdu](https://www.engage-csedu.org/)"),
    (r"{The POGIL Project}", "[The POGIL Project](https://www.pogil.org/)"),
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
            entry = parse_entry(bib_path)
            out = io.StringIO()
            write_entry(entry, out)
            markdown += out.getvalue()

    return markdown


def abbreviate(url):
    """Shorten the URL for better text wrapping."""
    pos = url.index("/", 8)
    return url[:pos+1] + "..."


def parse_entry(path):
    """Parse the given bib file and return the entry."""

    # Abort if the file format is incorrect
    library = bibtexparser.parse_file(path)
    n = len(library.failed_blocks)
    if n > 0:
        raise ValueError(f"{n} blocks failed to parse")
    n = len(library.entries)
    if n != 1:
        raise ValueError(f"{n} entries found (not 1)")
    return library.entries[0]


def write_entry(entry, out):
    """Output the given entry in Markdown format."""

    # Write the "Abstract" section if present
    field = entry.fields_dict.get("abstract")
    if field:
        out.write("\n## Abstract\n\n")
        out.write(field.value + "\n")

    # Write the "Contents" section if present
    field = entry.fields_dict.get("contents")
    if field:

        # Get the index after the left brace
        pattern = r"^\s*contents\s*=\s*{"
        match = re.search(pattern, entry.raw, re.MULTILINE)
        col = len(match.group())

        # Remove leading whitespace from each line
        lines = field.value.splitlines()
        for i in range(1, len(lines)):
            line = lines[i]
            beg = 0
            while beg < len(line) and beg < col and line[beg] == " ":
                beg += 1
            lines[i] = line[beg:]

        # The resulting lines are Markdown format
        out.write("\n## Contents\n\n")
        out.write("\n".join(lines) + "\n")

    # Write section heading and download link
    out.write("\n## Metadata\n\n")
    name = entry.key + ".bib"
    down = '{download="' + name + '"}'
    out.write(f"[:material-download: Download .bib file]({name}){down}\n\n")

    # Write field-value pairs in table format
    out.write("Field | Value\n------|------\n")
    for fkey, field in entry.fields_dict.items():
        if fkey in ["abstract", "contents"]:
            continue
        out.write(f"{fkey} | ")
        if fkey != "url":
            out.write(f"{field.value}\n")
        else:
            # Abbreviate the URL to allow text wrapping
            url = field.value
            abbr = abbreviate(url)
            out.write(f"[{abbr}]({url})\n")
