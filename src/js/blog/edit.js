onDocumentReady(() => {
  // Only apply this script to article edit pages.
  if (!document.body.classList.contains('article_edit')) {
    return
  }

  /** @type {HTMLFormElement | null} */
  const formElem = document.querySelector('.post_edit form[method="post"]')
  /** @type {HTMLElement | null} */
  const articleElem = document.querySelector('.post_edit article.preview')
  /** @type {HTMLButtonElement | null} */
  const togglePreviewButton = document.querySelector('.toggle_preview_button')
  const mainElem = document.getElementById('main')
  const editNavElem = mainElem ? mainElem.querySelector('nav') : null
  /** @type {HTMLInputElement | null} */
  // @ts-ignore
  const titleElem = document.getElementById('id_title')
  /** @type {HTMLTextAreaElement | null} */
  // @ts-ignore
  const contentElem = document.getElementById('id_content')
  /** @type {HTMLInputElement | null} */
  // @ts-ignore
  const slugElem = document.getElementById('id_slug')

  const editNavRect = editNavElem ? editNavElem.getBoundingClientRect() : null
  const originalNavTop = editNavRect
    ? editNavRect.top + window.pageYOffset - document.documentElement.clientTop
    : 0
  let navFixed = false
  /** @type {number | undefined} */
  let resizeTimeoutHandle
  let formScrollTop = 0
  let previewScrollTop = 0

  const switchToPreview = () => {
    // Remember where we had scrolled to.
    formScrollTop = document.documentElement.scrollTop

    if (togglePreviewButton) {
      togglePreviewButton.classList.add('toggled')
    }

    if (formElem) {
      formElem.style.display = 'none'
    }

    if (articleElem) {
      articleElem.style.display = 'block'
    }

    // Set back where we had scroll to.
    // We'll do this so we're looking at roughly the same thing
    // as we flip preview on and off.
    document.documentElement.scrollTop = previewScrollTop
  }

  const switchToForm = () => {
    previewScrollTop = document.documentElement.scrollTop

    if (togglePreviewButton) {
      togglePreviewButton.classList.remove('toggled')
    }

    if (articleElem) {
      articleElem.style.display = 'none'
    }

    if (formElem) {
      formElem.style.display = 'block'
    }

    document.documentElement.scrollTop = formScrollTop
  }

  const generatePreview = () => {
    if (!articleElem || !contentElem || !titleElem) {
      return
    }

    // Generate HTML with the JavaScript markdown parser.
    const html = marked(contentElem.value, {
      gfm: true,
      sanitize: false,
    })

    const title = titleElem.value || '<no title>'
    const postElem = articleElem.querySelector('.post')
    const articleTitleElem = articleElem.querySelector('header > h1')

    // Set the title of the article.
    if (articleTitleElem) {
      articleTitleElem.textContent = title
    }

    // Set produced HTML in the preview article.
    if (postElem) {
      postElem.innerHTML = html

      // Apply code highlighting to the generated text.
      HighlightCode.scan(postElem)
    }

    switchToPreview()
  }

  const adjustFixedNavHorizontal = () => {
    if (navFixed && mainElem && editNavElem) {
      const leftOffset = mainElem.getBoundingClientRect().left
        + window.pageXOffset - document.documentElement.clientLeft

      // The left margin is the same size as the right margin.
      editNavElem.style.right = leftOffset + 'px'
    }
  }

  if (togglePreviewButton) {
    togglePreviewButton.addEventListener('click', () => {
      if (togglePreviewButton.classList.contains('toggled')) {
        switchToForm()
      } else {
        generatePreview()
      }
    })
  }

  document.addEventListener('scroll', () => {
    if (window.pageYOffset > originalNavTop - 10) {
      if (!navFixed) {
        navFixed = true

        if (editNavElem) {
          editNavElem.classList.add('fixed_when_big')
        }

        adjustFixedNavHorizontal()
      }
    } else {
      if (navFixed) {
        navFixed = false

        if (editNavElem) {
          editNavElem.classList.remove('fixed_when_big')
        }
      }
    }
  })

  addEventListener('resize', () => {
    clearTimeout(resizeTimeoutHandle)

    resizeTimeoutHandle = setTimeout(() => {
      adjustFixedNavHorizontal()
    }, 100)
  })

  /** @type {(file: File, callback: (url: string) => void) => void} */
  const uploadFile = (file, callback) => {
    const body = new FormData()
    body.append('file', file, file.name)

    const cookieMatch = document.cookie.match(/csrftoken=([^;]+)/)
    const csrfToken = cookieMatch ? cookieMatch[1] : ''

    fetch('/blog/upload/', {
      method: 'POST',
      headers: {'X-CSRFToken': csrfToken},
      body,
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Upload failed')
        }

        return response.json()
      })
      .then(json => {
        callback(json.url)
      })
      .catch(err => {
        console.error(err)
      })
  }

  if (contentElem) {
    /** @type {(urlList: [string, string][]) => void} */
    const addFiles = urlList => {
      const selectionStart = contentElem.selectionStart
      const selectionEnd = contentElem.selectionEnd

      const textBefore = contentElem.value.slice(0, selectionStart)
      let textAfter = contentElem.value.slice(selectionEnd)
      let insertText = '\n' + urlList.map(([type, url]) => {
        if (type === 'audio/mpeg') {
          const audio = new Audio()
          audio.src = url

          return audio.outerHTML.replace('<audio', '<audio controls="controls"')
        } else {
        // The image will be pre-loaded here.
          const image = new Image()
          image.src = url

          const anchor = document.createElement('a')
          anchor.className = 'image-link'
          anchor.href = url
          anchor.target = '_blank'
          anchor.appendChild(image)

          return '<figure>'
          + '\n  ' + anchor.outerHTML
          + '\n  <figcaption></figcaption>'
          + '\n</figure>'
        }
      }).join('\n')

      if (!textBefore) {
        insertText = insertText.slice(2)
      }

      textAfter = textAfter.trim()

      if (textAfter) {
        insertText += '\n\n'
      }

      contentElem.value = textBefore + insertText + textAfter
    }

    // Highlight the content box on dragging.
    for (const eventName of ['dragover', 'dragenter', 'dragleave']) {
      contentElem.addEventListener(eventName, event => {
        event.preventDefault()
        event.stopPropagation()

        if (eventName === 'dragleave') {
          contentElem.classList.remove('drag-over')
        } else {
          contentElem.classList.add('drag-over')
        }
      })
    }

    contentElem.addEventListener('drop', event => {
      event.preventDefault()
      event.stopPropagation()

      contentElem.classList.remove('drag-over')

      const data = event.dataTransfer
      const files = Array.from(data && data.files ? data.files : [])
        .filter(file =>
          file.type === 'image/png'
          || file.type === 'image/jpeg'
          || file.type === 'image/gif'
          || file.type === 'audio/mpeg'
        )

      /** @type {[string, string][]} */
      const urlList = Array(files.length)
      urlList.fill(['', ''])

      files.forEach((file, index) => {
        uploadFile(file, (url) => {
          urlList[index] = [file.type, url]

          // Add images after all files have been uploaded.
          if (urlList.every((x) => Boolean(x))) {
            addFiles(urlList)
          }
        })
      })
    })
  }

  // Automatically set the slug based on the title changing.
  if (titleElem && slugElem) {
    for (const event of ['keyup', 'change']) {
      titleElem.addEventListener(event, () => {
        slugElem.value = titleElem.value.toLowerCase().replace(/[^a-zA-Z0-9]/g, '-')
      })
    }
  }
})
