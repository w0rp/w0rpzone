$(function() {
    "use strict";

    // Markdown previews.
    var $form = $('.comment_list form');
    var $preview_comment = $('.comment_list .comment.preview');
    var $name_field = $preview_comment.find(".post_metadata .name");
    var $comment_body = $preview_comment.children(".comment_body");

    var $show_preview_button = $form.find('button.show_preview');
    var $hide_preview_button = $preview_comment.find('button.hide_preview');

    function switch_to_preview() {
        $form.hide();
        $preview_comment.show();
    }

    function switch_to_form() {
        $preview_comment.hide();
        $form.show();
    }

    function generate_preview() {
        // Generate HTML with the JavaScript markdown parser.
        var html = marked($("#id_content").val(), {
            gfm: true,
            sanitize: true
        });

        $name_field.text(
            $("#id_poster_name").val()
            || $name_field.data("default-name")
        );

        $comment_body.html(html);

        // Apply code highlighting to the generated text.
        HighlightCode.scan($comment_body);

        switch_to_preview();
    }

    $show_preview_button.click(function() {
        generate_preview();
    });

    $hide_preview_button.click(function() {
        switch_to_form();
    });

    var $brief_help = $(".markdown_help.brief");
    var $full_help = $(".markdown_help.full");

    // Show and hide help information.
    $brief_help.find(".show_help").click(function(event) {
        event.preventDefault();

        $full_help.addClass("active");
        $brief_help.removeClass("active");
    });

    $full_help.find(".hide_help").click(function(event) {
        event.preventDefault();

        $brief_help.addClass("active");
        $full_help.removeClass("active");
    });

    var $help_tabs = $full_help.find(".help_tabs > .tab");
    var $help_topics = $full_help.find(".help_topic");

    // Switch between help topics by clicking the tabs.
    $help_tabs.click(function(event) {
        var $last_tab = $help_tabs.filter(".active");
        var $last_topic = $help_topics.filter("." + $last_tab.data("topic"));
        var $new_tab = $(this);
        var $new_topic = $help_topics.filter("." + $new_tab.data("topic"));

        $last_tab.removeClass("active");
        $last_topic.removeClass("active");
        $new_tab.addClass("active");
        $new_topic.addClass("active");
    });

    if ($form.hasClass("has_errors")) {
        // Scroll to the form when there are errors in it.
        $(window).scrollTop($form.closest('section').offset().top);
    }
});
