"""Make the site_name link to the home page."""


def on_post_page(output, page, config):
    """Called after the template is rendered."""

    # Get relative link to home page
    home_path = "../" * page.url.count("/")
    if home_path:
        # Remove the trailing slash
        home_path = home_path[:-1]
    else:
        # Special case: already home
        home_path = "."

    # Find and modify each instance
    logo = config["theme"]["logo"]
    name = config["site_name"]
    link = f'<a href="../../..">{name}</a>'
    beg = 0
    while (beg := output.find(logo, beg)) > -1:
        # Find site_name after the logo
        beg = output.index(name, beg)
        end = beg + len(name)
        output = output[:beg] + link + output[end:]

    return output
