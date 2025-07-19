document$.subscribe(function () {
  let tables = document.querySelectorAll("article table:not([class])");
  tables.forEach(function (table) {
    let div = table.parentElement.parentElement.parentElement;
    if (div.id.endsWith('-index')) {

      // Function to identify text content
      function setClass(child, name) {
        while (child.firstChild.tagName) {
          child = child.firstChild;
        }
        child.className = name;
      }

      // Add required classes after the fact
      let tbody = table.querySelector('tbody');
      tbody.className = 'list';
      let rows = tbody.querySelectorAll("tr");
      rows.forEach(row => {
        setClass(row.children[0], 'title');
        setClass(row.children[1], 'author');
        setClass(row.children[2], 'source');
        setClass(row.children[3], 'year');
      });

      // Set up pagination, searching, and sorting
      let options = {
        valueNames: ['title', 'author', 'source', 'year'],
        page: 10,
        pagination: true
      };
      let tableList = new List(div.id, options);

    }
  })
})
