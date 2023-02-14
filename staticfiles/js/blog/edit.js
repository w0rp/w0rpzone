/* global HighlightCode, marked */
$(() => {
  'use strict'

  if (!$(document.body).hasClass('article_edit')) {
    // Only apply this script to article edit pages.
    return
  }

  var $form = $('.post_edit form:first')
  var $article = $('.post_edit article.preview')
  var $togglePreviewButton = $('.toggle_preview_button')
  var $main = $('#main')
  var $editNav = $main.children('nav')
  const $title = $('#id_title')
  const $slug = $('#id_slug')

  var editNavOffset = $editNav.offset()
  var originalNavTop = editNavOffset ? editNavOffset.top : 0
  var navFixed = false
  /** @type {number | undefined} */
  var resizeTimeoutHandle
  var formScrollTop = 0
  var previewScrollTop = 0

  function switchToPreview() {
    // Remember where we had scrolled to.
    formScrollTop = document.documentElement.scrollTop

    $togglePreviewButton.addClass('toggled')
    $form.hide()
    $article.show()

    // Set back where we had scroll to.
    // We'll do this so we're looking at roughly the same thing
    // as we flip preview on and off.
    document.documentElement.scrollTop = previewScrollTop
  }

  function switchToForm() {
    previewScrollTop = document.documentElement.scrollTop

    $togglePreviewButton.removeClass('toggled')
    $article.hide()
    $form.show()

    document.documentElement.scrollTop = formScrollTop
  }

  function generatePreview() {
    // Generate HTML with the JavaScript markdown parser.
    var html = marked(String($('#id_content').val()), {
      gfm: true,
      sanitize: false,
    })

    var title = String($('#id_title').val() || '<no title>')
    var $post = $article.children('.post')

    // Set produced HTML in the preview article.
    $article.find('header > h1').text(title)
    $post.html(html)

    // Apply code highlighting to the generated text.
    HighlightCode.scan($post)

    switchToPreview()
  }

  function adjustFixedNavHorizontal() {
    if (!navFixed) {
      return
    }

    const mainOffset = $main.offset()

    if (mainOffset) {
      // The left margin is the same size as the right margin.
      $editNav.css('right', mainOffset.left)
    }
  }

  $togglePreviewButton.click(() => {
    if ($togglePreviewButton.hasClass('toggled')) {
      switchToForm()
    } else {
      generatePreview()
    }
  })

  $(window).scroll(() => {
    if (($(window).scrollTop() || 0) > originalNavTop - 10) {
      if (!navFixed) {
        navFixed = true

        $editNav.addClass('fixed_when_big')
        adjustFixedNavHorizontal()
      }
    } else {
      if (navFixed) {
        navFixed = false

        $editNav.removeClass('fixed_when_big')
      }
    }
  })

  $(window).resize(() => {
    clearTimeout(resizeTimeoutHandle)

    resizeTimeoutHandle = setTimeout(() => {
      adjustFixedNavHorizontal()
    }, 100)
  })

  var textArea = $('textarea[name="content"]')

  /** @type {(file: File, callback: (url: string) => void) => void} */
  function uploadFile(file, callback) {
    var data = new FormData()
    data.append('file', file, file.name)

    $.ajax({
      url: '/blog/upload/',
      data: data,
      type: 'POST',
      contentType: false,
      processData: false,
    }).done((data) => {
      callback(data.url)
    })
  }

  /** @type {(urlList: string[]) => void} */
  function addImages(urlList) {
    var selectionStart = textArea.prop('selectionStart')
    var selectionEnd = textArea.prop('selectionEnd')

    var textBefore = String(textArea.val()).slice(0, selectionStart)
    var textAfter = String(textArea.val()).slice(selectionEnd)
    var insertText = urlList.map((url) => {
      // The image will be pre-loaded here.
      var image = new Image()
      image.src = url

      var anchor = document.createElement('a')
      anchor.className = 'image-link'
      anchor.href = url
      anchor.target = '_blank'
      anchor.appendChild(image)

      return '\n\n<figure>'
        + '\n  ' + anchor.outerHTML
        + '\n  <figcaption></figcaption>'
        + '\n</figure>'
    }).join('')

    if (!textBefore) {
      insertText = insertText.slice(2)
    }

    textAfter = textAfter.trim()

    if (textAfter) {
      insertText += '\n\n'
    }

    textArea.val(textBefore + insertText + textAfter)
  }

  textArea.on('dragover dragenter', (event) => {
    event.preventDefault()
    event.stopPropagation()

    textArea.addClass('drag-over')
  })

  textArea.on('dragleave', (event) => {
    event.preventDefault()
    event.stopPropagation()

    textArea.removeClass('drag-over')
  })

  // @ts-ignore
  textArea.on('drop', /** @type {(event: JQueryEventObject & {originalEvent: DragEvent}) => void} */ (event) => {
    event.preventDefault()
    event.stopPropagation()

    textArea.removeClass('drag-over')

    var data = event.originalEvent.dataTransfer
    var files = Array.from(data && data.files ? data.files : [])
      .filter(file =>
        file.type === 'image/png'
        || file.type === 'image/jpeg'
        || file.type === 'image/gif'
      )

    /** @type {string[]} */
    var urlList = Array(files.length)
    urlList.fill('')

    files.forEach((file, index) => {
      uploadFile(file, (url) => {
        urlList[index] = url

        // Add images after all files have been uploaded.
        if (urlList.every((x) => Boolean(x))) {
          addImages(urlList)
        }
      })
    })
  })

  // Automatically set the slug based on the title changing.
  $title.on('keyup change', () => {
    const text = ($title.val() || '').toString()

    $slug.val(text.toLowerCase().replace(/[^a-zA-Z0-9]/g, '-'))
  })
})
