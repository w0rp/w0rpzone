onDocumentReady(() => {
  // Markdown previews.
  /** @type {HTMLFormElement | null} */
  const formElem = document.querySelector('.comment_list form')
  /** @type {HTMLElement | null} */
  const previewCommentElem = document.querySelector('.comment_list .comment.preview')
  /** @type {HTMLElement | null} */
  const nameFieldElem = previewCommentElem
    ? previewCommentElem.querySelector('.post_metadata .name')
    : null
  /** @type {HTMLElement | null} */
  const commentBodyElem = previewCommentElem
    ? previewCommentElem.querySelector('.comment_body')
    : null

  /** @type {HTMLButtonElement | null} */
  const showPreviewButton = formElem
    ? formElem.querySelector('button.show_preview')
    : null
  /** @type {HTMLButtonElement | null} */
  const hidePreviewButton = previewCommentElem
    ? previewCommentElem.querySelector('button.hide_preview')
    : null

  const switchToPreview = () => {
    if (formElem) {
      formElem.style.display = 'none'
    }

    if (previewCommentElem) {
      previewCommentElem.style.display = 'block'
    }
  }

  const switchToForm = () => {
    if (previewCommentElem) {
      previewCommentElem.style.display = 'none'
    }

    if (formElem) {
      formElem.style.display = 'block'
    }
  }

  const generatePreview = () => {
    /** @type {HTMLTextAreaElement | null} */
    // @ts-ignore
    const contentElem = document.getElementById('id_content')

    /** @type {HTMLInputElement | null} */
    // @ts-ignore
    const posterNameElem = document.getElementById('id_poster_name')

    // Generate HTML with the JavaScript markdown parser.
    const html = marked(contentElem ? contentElem.value : '', {
      gfm: true,
      sanitize: true,
    })

    if (nameFieldElem) {
      nameFieldElem.textContent = posterNameElem ? posterNameElem.value : ''
    }

    if (commentBodyElem) {
      commentBodyElem.innerHTML = html

      // Apply code highlighting to the generated text.
      HighlightCode.scan(commentBodyElem)
    }

    switchToPreview()
  }

  if (showPreviewButton) {
    showPreviewButton.addEventListener('click', () => {
      generatePreview()
    })
  }

  if (hidePreviewButton) {
    hidePreviewButton.addEventListener('click', () => {
      switchToForm()
    })
  }

  /** @type {HTMLElement | null} */
  const briefHelpElem = document.querySelector('.markdown_help.brief')
  /** @type {HTMLElement | null} */
  const fullHelpElem = document.querySelector('.markdown_help.full')

  if (briefHelpElem && fullHelpElem) {
    /** @type {HTMLElement | null} */
    const showHelpElem = briefHelpElem.querySelector('.show_help')
    /** @type {HTMLElement | null} */
    const hideHelpElem = fullHelpElem.querySelector('.hide_help')

    // Show and hide help information.
    if (showHelpElem) {
      showHelpElem.addEventListener('click', event => {
        event.preventDefault()

        fullHelpElem.classList.add('active')
        briefHelpElem.classList.remove('active')
      })
    }

    if (hideHelpElem) {
      hideHelpElem.addEventListener('click', event => {
        event.preventDefault()

        briefHelpElem.classList.add('active')
        fullHelpElem.classList.remove('active')
      })
    }

    /** @type {NodeListOf<HTMLButtonElement>} */
    const helpTabElems = fullHelpElem.querySelectorAll('.help_tabs > .tab')
    /** @type {NodeListOf<HTMLElement>} */
    const helpTopicElems = fullHelpElem.querySelectorAll('.help_topic')

    /** @type {(nodeList: NodeListOf<HTMLElement>, className: string) => HTMLElement | null} */
    const findElemWithClass = (nodeList, className) => Array.from(nodeList)
      .find(e => e.classList.contains(className)) || null

    // Switch between help topics by clicking the tabs.
    helpTabElems.forEach(newTabElem => {
      newTabElem.addEventListener('click', () => {
        const lastTabElem = findElemWithClass(helpTabElems, 'active')

        if (!lastTabElem) {
          throw new Error('last tab not found!')
        }

        const lastTopicElem = findElemWithClass(
          helpTopicElems,
          lastTabElem.getAttribute('data-topic') || ''
        )
        const newTopicElem = findElemWithClass(
          helpTopicElems,
          newTabElem.getAttribute('data-topic') || ''
        )

        lastTabElem.classList.remove('active')
        newTabElem.classList.add('active')

        if (lastTopicElem) {
          lastTopicElem.classList.remove('active')
        }

        if (newTopicElem) {
          newTopicElem.classList.add('active')
        }
      })
    })
  }

  // Scroll to the form when there are errors in it.
  if (formElem && formElem.classList.contains('has_errors')) {
    const section = formElem.closest('section')
    const rect = section
      ? section.getBoundingClientRect()
      : null
    const top = rect
      ? rect.top + window.pageYOffset - document.documentElement.clientTop
      : 0

    if (top) {
      window.scrollTo({top})
    }
  }
})
