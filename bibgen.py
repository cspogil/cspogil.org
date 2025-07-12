"""Parse all BibTeX files and generate Markdown for each entry."""

import bibtexparser
import glob
import os


def reformat_authors(author_string):
    """Convert author string to "First Last" format, separated by commas."""
    authors = author_string.split(" and ")
    reformatted = []
    for author in authors:
        if "," in author:
            last, first = [part.strip() for part in author.split(",", 1)]
            reformatted.append(f"{first} {last}")
        else:
            # Already in "First Last" format
            reformatted.append(author.strip())
    return ", ".join(reformatted)


def bib2md(path, entry):
    """Generate a Markdown file for the entry."""

    # Extract the most common fields
    title = entry.fields_dict["title"].value
    author = entry.fields_dict["author"].value
    year = entry.fields_dict["year"].value
    source = ""
    for fkey in ["booktitle", "journal", "publisher", "howpublished", "url"]:
        if fkey in entry.fields_dict:
            source = entry.fields_dict[fkey].value
            break

    # Create a reference format string
    author = reformat_authors(author)
    if source:
        source = f"*{source}*."
        if entry.entry_type.startswith("in"):
            source = "In " + source
    ref = f"{author}. ({year}). {title}. {source}"

    # Generate code for download link
    name = os.path.basename(path)
    down = '{download="' + name + '"}'

    # Generate corresponding Markdown file
    with open(path[:-3] + "md", "w") as file:
        file.write("---\nhide:\n  - toc\n---\n\n")
        file.write(f"# {title}\n\n")
        file.write(f"**Reference:** {ref}\n\n")
        file.write('<div class="grid" markdown="1">\n\n')
        file.write(f"**Entry Key:** `#!tex \\cite{{{entry.key}}}`\n\n")
        file.write(f"**Entry Type:** `@{entry.entry_type}`\n\n")
        file.write("</div>\n\n")
        file.write(f"[:material-download: Download .bib file]({name}){down}\n\n")
        file.write("## Metadata\n\n")

        # Render the BiBTeX fields as a table
        contents = ""
        file.write("Field | Value\n------|------\n")
        for fkey, field in entry.fields_dict.items():
            if fkey != "contents":
                file.write(f"{fkey} | {field.value}\n")
            else:
                # Remove leading whitespace from every line
                contents = "\n".join(line.lstrip() for line in field.value.splitlines())
        if contents:
            file.write("\n## Contents\n\n")
            file.write(contents + "\n")


def main():
    """Find and parse every bib file."""
    for path in glob.glob("docs/**/*.bib", recursive=True):
        print(path)
        library = bibtexparser.parse_file(path)
        if len(library.failed_blocks) > 0:
            print("Warning: Some blocks failed to parse")
        for entry in library.entries:
            bib2md(path, entry)


if __name__ == "__main__":
    main()
