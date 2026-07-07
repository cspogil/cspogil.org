// Copy section contents from the nav and append to article

(function () {
  const navList = document.querySelector('li.md-nav__item--active ul.md-nav__list');
  if (navList) {
    const article = document.querySelector('article');
    const section = document.createElement("section");
    section.className = "auto-index";
    const clone = navList.cloneNode(true);
    article.appendChild(section);
    section.appendChild(clone);
  }
})();
