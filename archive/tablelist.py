def gen_table(name, entries_dict):
    """Generate a Markdown table for the given entires."""
    path = f"tables/{name}.md"
    with open(path, "w") as file:
        file.write(WARN + "\n\n")
        file.write(f'<div id="{name}-index" markdown="1">\n\n')

        # Inputs
        file.write('<div>\n')
        file.write('<input id="filter" class="search" type="search" placeholder="Filter...">\n')
        file.write('<ul class="pagination"></ul>\n')
        file.write('</div>\n\n')

        # Table head
        file.write('<button class="sort" data-sort="title">Title</button> | ')
        file.write('<button class="sort" data-sort="author">Author</button> | ')
        file.write('<button class="sort" data-sort="source">Source</button> | ')
        file.write('<button class="sort" data-sort="year">Year</button>\n')
        file.write("-----|-----|-----|-----\n")

        # Table body
        items = sorted(entries_dict.items(), key=sort_key)
        for href, entry in items:
            author, year, title, source = get_fields(entry)
            link = f"[{title}]({href})"
            file.write(f"{link} | {author} | {source} | {year}\n")

        file.write('\n</div>\n')
