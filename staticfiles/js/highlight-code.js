/* Public domain, created by w0rp */
// eslint-disable-next-line
;(() => {
  'use strict'

  /** @type {(list: string[]) => RegExp} */
  function createOrRegex(list) {
    return new RegExp('^(' + list.join('|') + ')$')
  }

  var keywordRegex = createOrRegex([
    '[$a-zA-Z_][a-zA-Z0-9_]*',
    '[a-zA-Z_][a-zA-Z0-9_]*<.*>',
    'v:true',
    'v:false',
    'v:null',
    '@nogc',
    '@disable',
  ])
  var variableRegex = createOrRegex([
    '[glasvbwt]:[a-zA-Z0-9_]*',
  ])
  var numberRegex = /^([0-9]+|[0-9]+.[0-9]+)$/

  window.HighlightCode = {
    scan: function(selector) {
      var $root = selector != null ? $(selector) : $(document.body)

      $root.find('pre code:not(.highlight)').each(function() {
        $(this).addClass('highlight')

        // Now apply the highlight after attempting to set the language.
        hljs.highlightBlock(this)
      })

      // Look for code elements which look like keywords, and highlight them
      // with keywords.
      $root.find('code:not(.highlight)').each(function() {
        var elem = $(this)
        var text = elem.text()
        var specialClass

        if (text.match(keywordRegex)) {
          specialClass = 'hljs-keyword'
        } else if (text.match(variableRegex)) {
          specialClass = 'hljs-variable'
        } else if (text.match(numberRegex)) {
          specialClass = 'hljs-number'
        }

        if (specialClass) {
          elem.addClass('highlight')

          var span = $(document.createElement('span'))
          span.addClass(specialClass)
          span.text(elem.text())
          elem.html(span[0])
        }
      })

      $root.find('td code:not(.highlight)').each(function() {
        $(this).addClass('highlight')
        hljs.highlightBlock(this)
        $(this).removeClass('hljs')
      })

      $root.find('p code:not(.highlight)').each(function() {
        $(this).addClass('highlight')
        hljs.highlightBlock(this)
      })
    },
  }
})()

$(() => {
  'use strict'

  HighlightCode.scan()
})
