'use strict';

{{ $searchDataFile := printf "%s.search-data.json" .Language.Lang }}
{{ $searchData := resources.Get "search-data.json" | resources.ExecuteAsTemplate $searchDataFile . | resources.Minify | resources.Fingerprint }}
{{ $searchConfig := i18n "bookSearchConfig" | default "{}" }}

(function () {
  const searchDataURL = '{{ $searchData.RelPermalink }}';
  const indexConfig = Object.assign({{ $searchConfig }}, {
    tokenize: "forward",
    optimize: true,
    resolution: 9,
    cache: 100,
    worker: true,
    document: {
      id: 'id',
      index: ['content'],
      store: ['title', 'href', 'section', 'content'],
    }
  });

  const input = document.querySelector('#book-search-input');
  const results = document.querySelector('#book-search-results');

  if (!input) {
    return
  }

  input.addEventListener('focus', init);
  input.addEventListener('keyup', search);

  document.addEventListener('keypress', focusSearchFieldOnKeyPress);

  /**
   * @param {Event} event
   */
  function focusSearchFieldOnKeyPress(event) {
    if (event.target.value !== undefined) {
      return;
    }

    if (input === document.activeElement) {
      return;
    }

    const characterPressed = String.fromCharCode(event.charCode);
    if (!isHotkey(characterPressed)) {
      return;
    }

    input.focus();
    event.preventDefault();
  }

  /**
   * @param {String} character
   * @returns {Boolean} 
   */
  function isHotkey(character) {
    const dataHotkeys = input.getAttribute('data-hotkeys') || '';
    return dataHotkeys.indexOf(character) >= 0;
  }

  function init() {
    input.removeEventListener('focus', init); // init once
    input.required = true;

    fetch(searchDataURL)
      .then(pages => pages.json())
      .then(pages => {
        window.bookSearchIndex = new FlexSearch.Document(indexConfig);
        pages.forEach(page => {
          window.bookSearchIndex.add(page.id, page);
        });
      })
      .then(() => input.required = false)
      .then(search);
  }

  function search() {
    while (results.firstChild) {
      results.removeChild(results.firstChild);
    }

    if (!input.value) {
      return;
    }

    const searchHits = window.bookSearchIndex.searchAsync(input.value, 5);
    searchHits.then(pages => {
      pages.forEach(function (pageMeta) {
        pageMeta.result.forEach(function (pageIdx) {
          console.log("Index: " + pageIdx)
          const page = window.bookSearchIndex.store[pageIdx];
          console.log(page)
          const li = element('<li><a href></a><small></small><br><medium></medium></li>');
          const a = li.querySelector('a'), small = li.querySelector('small'), medium = li.querySelector('medium');
    
          a.href = page.href;
          a.textContent = page.title;
          small.textContent = page.section;
    
          console.log(page)
          const idx = page.content.indexOf(input.value);
          if (idx > 0) {
            // Bold the search term
            let content = page.content.substring(0, idx) + '<strong>' + page.content.substring(idx, idx + input.value.length) + '</strong>' + page.content.substring(idx + input.value.length);
    
            let start = idx - (100-input.value.length)/2;
            if (start < 0) {
              start = 0;
            }
            let end = idx + input.value.length + (100-input.value.length)/2;
            if (end > content.length) {
              end = content.length;
            }
            medium.innerHTML = "..." + content.substring(start, end) + "...";
            results.appendChild(li);
          }
        });
      });
    });
  }

  /**
   * @param {String} content
   * @returns {Node}
   */
  function element(content) {
    const div = document.createElement('div');
    div.innerHTML = content;
    return div.firstChild;
  }
})();
