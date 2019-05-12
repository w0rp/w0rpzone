$(() => {
  'use strict'

  /* global HighlightCode */

  // Markdown previews.
  var $form = $('.comment_list form')
  var $previewComment = $('.comment_list .comment.preview')
  var $nameField = $previewComment.find('.post_metadata .name')
  var $commentBody = $previewComment.children('.comment_body')

  var $showPreviewButton = $form.find('button.show_preview')
  var $hidePreviewButton = $previewComment.find('button.hide_preview')

  function switchToPreview() {
    $form.hide()
    $previewComment.show()
  }

  function switchToForm() {
    $previewComment.hide()
    $form.show()
  }

  function generatePreview() {
    // Generate HTML with the JavaScript markdown parser.
    var html = marked($('#id_content').val(), {
      gfm: true,
      sanitize: true,
    })

    $nameField.text($('#id_poster_name').val())

    $commentBody.html(html)

    // Apply code highlighting to the generated text.
    HighlightCode.scan($commentBody)

    switchToPreview()
  }

  $showPreviewButton.click(() => {
    generatePreview()
  })

  $hidePreviewButton.click(() => {
    switchToForm()
  })

  var $briefHelp = $('.markdown_help.brief')
  var $fullHelp = $('.markdown_help.full')

  // Show and hide help information.
  $briefHelp.find('.show_help').click((event) => {
    event.preventDefault()

    $fullHelp.addClass('active')
    $briefHelp.removeClass('active')
  })

  $fullHelp.find('.hide_help').click((event) => {
    event.preventDefault()

    $briefHelp.addClass('active')
    $fullHelp.removeClass('active')
  })

  var $helpTabs = $fullHelp.find('.helpTabs > .tab')
  var $helpTopics = $fullHelp.find('.help_topic')

  // Switch between help topics by clicking the tabs.
  $helpTabs.click(function() {
    var $lastTab = $helpTabs.filter('.active')
    var $lastTopic = $helpTopics.filter('.' + $lastTab.data('topic'))
    var $newTab = $(this)
    var $newTopic = $helpTopics.filter('.' + $newTab.data('topic'))

    $lastTab.removeClass('active')
    $lastTopic.removeClass('active')
    $newTab.addClass('active')
    $newTopic.addClass('active')
  })

  if ($form.hasClass('has_errors')) {
    // Scroll to the form when there are errors in it.
    $(window).scrollTop($form.closest('section').offset().top)
  }
})
