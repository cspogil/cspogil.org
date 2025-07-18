# BibTeX Generator

Use this tool to generate a .bib file for an activity collection.
All fields are optional except the key.

## Input

<style>
  #bg_form {
    display: grid;
    grid-template-columns: max-content 1fr;
    gap: 0.5rem 1rem;
  }
  textarea {
    padding: 1ex;
    overflow-y: hidden;
    resize: none;
  }
</style>

<div id="bg_form" class="annotate">

  <label for="bg_key">Cite Key</label>
  <textarea id="bg_key" rows="1"></textarea>

  <label for="bg_author">Author (1)</label>
  <textarea id="bg_author" rows="1"></textarea>

  <label for="bg_title">Title</label>
  <textarea id="bg_title" rows="1"></textarea>

  <label for="bg_how">How Publ.</label>
  <textarea id="bg_how" rows="1"></textarea>

  <label for="bg_url">URL</label>
  <textarea id="bg_url" rows="1"></textarea>

  <label for="bg_month">Month</label>
  <textarea id="bg_month" rows="1"></textarea>

  <label for="bg_year">Year</label>
  <textarea id="bg_year" rows="1"></textarea>

  <label for="bg_note">Note</label>
  <textarea id="bg_note" rows="1"></textarea>

  <label for="bg_contents">Contents (2)</label>
  <textarea id="bg_contents" rows="3"></textarea>

</div>

1. Separate multiple authors with `and`. For example:<br>
   Richard S. Moog **and** Marcy Dubroff **and** Julie Boldizar **and** Sully

2. Additional information about the collection, such as the table of contents.
   Markdown syntax is supported.

## Output

```
```

<a id="bg_download" href="unnamed.bib">
  :material-download: Download .bib file
</a>

<script src="../bibgen.js?v=2025-07-12"></script>
