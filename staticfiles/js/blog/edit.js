$(function() {
    "use strict";

    var $form = $('.post_edit form:first');
    var $article = $('.post_edit article.preview');
    var $toggle_preview_button = $('.toggle_preview_button');

    function switch_to_preview() {
        $toggle_preview_button.addClass("toggled");
        $form.hide();
        $article.show();
    }

    function switch_to_form() {
        $toggle_preview_button.removeClass("toggled");
        $article.hide();
        $form.show();
    }

    function generate_preview() {
        $form.addClass("busy");

        // Send markdown content to the server-side parser.
        $.ajax({
            url: "/blog/preview-markdown/",
            type: "POST",
            dataType: "html",
            data: {
                text: $("#id_content").val()
            },
            error: function() {
                $form.removeClass("busy");

                // TODO: Handle request errors.
            },
            success: function(html) {
                $form.removeClass("busy");

                var title = $("#id_title").val() || "<no title>";
                var $post = $article.children(".post");

                // Set produced HTML in the preview article.
                $article.find("header > h1").text(title);
                $post.html(html);

                // Apply code highlighting to the generated text.
                HighlightCode.scan($post);

                switch_to_preview();
            }
        });
    }

    $toggle_preview_button.click(function() {
        if ($toggle_preview_button.hasClass("toggled")) {
            switch_to_form();
        } else {
            generate_preview();
        }
    });
});
