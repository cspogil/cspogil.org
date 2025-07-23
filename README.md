# cspogil.org

The website is built with [MkDocs][1] using the [Material][2] theme and [Awesome Nav][3] plugin.
Deployment to [GitHub Pages][4] is automated via [GitHub Actions][5].

[1]: https://www.mkdocs.org/
[2]: https://squidfunk.github.io/mkdocs-material/
[3]: https://lukasgeiter.github.io/mkdocs-awesome-nav/
[4]: https://pages.github.com/
[5]: https://github.com/features/actions

## Dev Setup

Create a Python virtual environment:
``` sh
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate.bat
```

Install the required Python packages:
``` sh
$ pip install --upgrade pip
$ pip install --pre -r requirements.txt
```

## Using MkDocs

To preview the site locally while editing:
``` sh
$ mkdocs serve
```

Then open http://127.0.0.1:8000/ in your browser.
Whenever you save a file under the docs directory, the site will automatically reload.

## References

* [Basic Syntax | Markdown Guide](https://www.markdownguide.org/basic-syntax/)
* [Reference - Material for MkDocs](https://squidfunk.github.io/mkdocs-material/reference/)
* [Reference - Awesome Nav for MkDocs](https://lukasgeiter.github.io/mkdocs-awesome-nav/reference/)

## Acknowledgments

* light-bulb.png is [Light Bulb free icon](https://www.flaticon.com/free-icon/light-bulb_2779262) by Freepik.
  Free for personal and commercial purpose with attribution.
* favicon.ico was created with:
  `convert light-bulb.png -define icon:auto-resize=64,48,32,16 favicon.ico`
