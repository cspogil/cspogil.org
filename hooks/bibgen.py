"""Parse BibTeX files and generate Markdown for each entry."""

import bibtexparser
import glob

LIBS = []

PUB = """
**{key}**<br>
{fields[title].value}
"""


def on_files(files, config):
    """Called after the files collection is populated from the docs_dir."""
    LIBS.clear()
    for path in glob.glob("docs/bib/*.bib"):
        LIBS.append(bibtexparser.parse_file(path))


def on_page_markdown(markdown, page, config, files):
    """Called after the page's markdown is loaded from the source file."""

    if page.url.startswith("research/"):
        for library in LIBS:
            for entry in library.entries:
                markdown += bib2md(entry)
        return markdown


def bib2md(entry):
    """Generate markdown for the given BibTeX entry."""
    return PUB.format(key=entry.key, fields=entry.fields_dict)
