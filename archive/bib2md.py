"""Parse all BibTeX files and generate Markdown for each entry."""

import glob
import os


def gen_md_file(path, entry):
    """Generate a Markdown file for the entry (publication)."""

    # Rename files to match the key
    name = os.path.basename(path)
    if name != entry.key + ".bib":
        new_name = entry.key + ".bib"
        new_path = path[:-len(name)] + new_name
        os.rename(path, new_path)
        md_path = path[:-3] + "md"
        if os.path.exists(md_path):
            os.rename(md_path, new_path[:-3] + "md")
        path = new_path
        name = new_name


def main():
    """Generate md files and index pages."""
    acts = {}
    pubs = {}

    # Find and parse every bib file
    for path in sorted(glob.glob("docs/**/*.bib", recursive=True)):
        print(path)
        entry = parse_entry(path)
        if path.startswith("docs/research"):
            gen_md_file(path, entry)

            # Relative path from index page
            href = path[14:-3] + "md"
            pubs[href] = entry
        else:
            href = path[16:-3] + "md"
            acts[href] = entry

    # Generate the index pages
    gen_table("activities", acts)
    gen_table("research", pubs)


if __name__ == "__main__":
    main()
