$(function() {
    "use strict";

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

    $(window).resize(function(event) {
        clearTimeout(resize_timeout_handle);

        resize_timeout_handle = setTimeout(function() {
            adjust_fixed_nav_horizontal();
        }, 100);
    });
});
