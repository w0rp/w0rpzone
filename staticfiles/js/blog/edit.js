/* global HighlightCode, marked */
$(function() {
    "use strict";

    if (!$(document.body).hasClass("article_edit")) {
        // Only apply this script to article edit pages.
        return;
    }

    var $form = $('.post_edit form:first');
    var $article = $('.post_edit article.preview');
    var $toggle_preview_button = $('.toggle_preview_button');
    var $main = $("#main");
    var $edit_nav = $main.children("nav");
    var original_nav_top = $edit_nav.offset().top;
    var nav_fixed = false;
    var resize_timeout_handle = null;
    var form_scroll_top = 0;
    var preview_scroll_top = 0;

    function switch_to_preview() {
        // Remember where we had scrolled to.
        form_scroll_top = document.documentElement.scrollTop;

        $toggle_preview_button.addClass("toggled");
        $form.hide();
        $article.show();

        // Set back where we had scroll to.
        // We'll do this so we're looking at roughly the same thing
        // as we flip preview on and off.
        document.documentElement.scrollTop = preview_scroll_top;
    }

    function switch_to_form() {
        preview_scroll_top = document.documentElement.scrollTop;

        $toggle_preview_button.removeClass("toggled");
        $article.hide();
        $form.show();

        document.documentElement.scrollTop = form_scroll_top;
    }

    function generate_preview() {
        // Generate HTML with the JavaScript markdown parser.
        var html = marked($("#id_content").val(), {
            gfm: true,
            sanitize: false
        });

        var title = $("#id_title").val() || "<no title>";
        var $post = $article.children(".post");

        // Set produced HTML in the preview article.
        $article.find("header > h1").text(title);
        $post.html(html);

        // Apply code highlighting to the generated text.
        HighlightCode.scan($post);

        switch_to_preview();
    }

    function adjust_fixed_nav_horizontal() {
        if (!nav_fixed) {
            return;
        }

        // The left margin is the same size as the right margin.
        $edit_nav.css("right", $main.offset().left);
    }

    $toggle_preview_button.click(function() {
        if ($toggle_preview_button.hasClass("toggled")) {
            switch_to_form();
        } else {
            generate_preview();
        }
    });

    $(window).scroll(function() {
        if ($(window).scrollTop() > original_nav_top - 10) {
            if (!nav_fixed) {
                nav_fixed = true;

                $edit_nav.addClass("fixed_when_big");
                adjust_fixed_nav_horizontal();
            }
        } else {
            if (nav_fixed) {
                nav_fixed = false;

                $edit_nav.removeClass("fixed_when_big");
            }
        }
    });

    $(window).resize(function() {
        clearTimeout(resize_timeout_handle);

        resize_timeout_handle = setTimeout(function() {
            adjust_fixed_nav_horizontal();
        }, 100);
    });

    var textArea = $('textarea[name="content"]');

    function uploadFile(file, callback) {
        var data = new FormData();
        data.append('file', file, file.name);

        $.ajax({
            url: '/blog/upload/',
            data: data,
            type: 'POST',
            contentType: false,
            processData: false,
        }).done(function(data) {
            callback(data.url);
        });
    }

    function addImages(urlList) {
        var selectionStart = textArea.prop('selectionStart')
        var selectionEnd = textArea.prop('selectionEnd')

        var textBefore = textArea.val().slice(0, selectionStart)
        var textAfter = textArea.val().slice(selectionEnd)
        var insertText = urlList.map(function(url) {
          // The image will be pre-loaded here.
          var image = new Image();
          image.src = url;

          var anchor = document.createElement('a')
          anchor.className = 'image-link';
          anchor.href = url;
          anchor.target = '_blank';
          anchor.appendChild(image);

          return '\n\n<figure>'
            + '\n  ' + anchor.outerHTML
            + '\n  <figcaption></figcaption>'
            + '\n</figure>';
        }).join('');

        if (!textBefore) {
          insertText = insertText.slice(2);
        }

        textAfter = textAfter.trim();

        if (textAfter) {
          insertText += '\n\n';
        }

        textArea.val(textBefore + insertText + textAfter);
    }

    textArea.on("dragover dragenter", function(event) {
        event.preventDefault();
        event.stopPropagation();

        textArea.addClass('drag-over');
    })

    textArea.on("dragleave", function(event) {
        event.preventDefault();
        event.stopPropagation();

        textArea.removeClass('drag-over');
    })

    textArea.on("drop", function(event) {
        event.preventDefault();
        event.stopPropagation();

        textArea.removeClass('drag-over');

        var data = event.originalEvent.dataTransfer;
        var files = Array.from(data && data.files ? data.files : [])
            .filter(function(file) {
                return file.type === 'image/png'
                    || file.type === 'image/jpeg'
                    || file.type === 'image/gif';
            });

        var urlList = Array(files.length);
        urlList.fill(undefined);

        files.forEach(function(file, index) {
            uploadFile(file, function(url) {
                urlList[index] = url;

                // Add images after all files have been uploaded.
                if (urlList.every(function(x) { return Boolean(x) })) {
                    addImages(urlList);
                }
            });
        });
    })
});
