function bibgen_init() {
  const bg_key = document.getElementById('bg_key');
  const bg_author = document.getElementById('bg_author');
  const bg_title = document.getElementById('bg_title');
  const bg_how = document.getElementById('bg_how');
  const bg_url = document.getElementById('bg_url');
  const bg_month = document.getElementById('bg_month');
  const bg_year = document.getElementById('bg_year');
  const bg_note = document.getElementById('bg_note');
  const bg_contents = document.getElementById('bg_contents');
  const bg_code = document.querySelector('pre > code');
  const bg_download = document.getElementById('bg_download');

  // Update output whenever input changes
  document.querySelectorAll('textarea').forEach(textarea => {
    textarea.addEventListener('input', () => {
      textarea.style.minHeight = 0;
      textarea.style.minHeight = textarea.scrollHeight + 2 + 'px';
      generate();
    });
  });

  // Function to download the bib file
  bg_download.addEventListener('click', (event) => {
    event.preventDefault();
    const name = bg_key.value;
    if (!name) {
      alert('Cite Key is required');
      return;
    }
    const blob = new Blob([bg_code.innerText], { type: 'text/plain' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = name + '.bib';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(link.href);
  });

  // Function to build the output string
  function generate() {
    const fields = [
      ['author', bg_author],
      ['title', bg_title],
      ['howpublished', bg_how],
      ['url', bg_url],
      ['month', bg_month],
      ['year', bg_year],
      ['note', bg_note],
    ];

    // Calculate equal sign alignment
    let width = 0;
    for (const [name, element] of fields) {
      if (element.value) {
        width = Math.max(width, name.length);
      }
    }
    if (bg_contents.value) {
      width = Math.max(width, 8);
    }

    // Append non-blank fields
    bg_code.innerText = `@misc{${bg_key.value.trim()},`;
    for (const [name, element] of fields) {
      if (element.value) {
        bg_code.innerText += `\n  ${name.padEnd(width)} = {${element.value.trim()}},`;
      }
    }

    // Append the contents block
    if (bg_contents.value) {
      const padded = bg_contents.value
        .split('\n')
        .map((line, index) => index === 0 ? line.trimEnd()
          : ' '.repeat(width + 6) + line.trimEnd())
        .join('\n');
      const name = 'contents';
      bg_code.innerText += `\n  ${name.padEnd(width)} = {${padded}}`;
    }
    bg_code.innerText += `\n}\n`;

    // Update the download link
    bg_download.href = bg_key.value ? bg_key.value + '.bib' : 'unnamed.bib';
  }

  generate();
}

bibgen_init();
