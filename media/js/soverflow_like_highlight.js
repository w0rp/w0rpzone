/* Public domain, created by w0rp */
$(function() {
    "use strict";

    var lang_re = /^\s*language: *([^ *]+) */;

    $("pre code").each(function() {
        // Step backwards to find the first non-text element.
        var elem = $(this).closest("pre")[0].previousSibling;

        while (elem != null && elem instanceof Text) {
            elem = elem.previousSibling;
        }

        if (elem instanceof Comment) {
            // Aha! We found a comment before the pre element.
            var match = elem.textContent.match(lang_re);

            if (match != null) {
                // Aha! It held our funky language semantic information.
                // Apply that as a class for the benefit of highlight.js
                $(this).addClass(match[1]);
            }
        }

        // Now apply the highlight after attempting to set the language.
        hljs.highlightBlock(this);
    });
});
