/* Public domain, created by w0rp */
function HighlightCode() {
    "use strict";

    // Escape a string for use in a regular expression.
    function escape_regex(string) {
        return string.replace(/[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]/g, "\\$&");
    }

    // Creates an OR regex from a list of strings.
    // The strings will be escaped.
    function regex_from_list(list) {
        var new_list = new Array(list.length);

        for (var i = 0; i < list.length; ++i) {
            new_list[i] = escape_regex(list[i]);
        }

        return new RegExp(new_list.join("|"));
    }

    var module = HighlightCode;

    // Build a list of symbols to look for to match a language as D.
    var d_regex = regex_from_list([
        "@safe",
        "@system",
        "@trusted",
        "nothrow",
        "pure",
        "@nogc",
        "Exception",
        "Error",
    ]);

    var lang_re = /^\s*language: *([^ *]+) */;

    module.scan = function(selector) {
        var $root = selector != null ? $(selector) : $(document);

        $root.find("pre code").each(function() {
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

            $(this).addClass("highlight");

            // Now apply the highlight after attempting to set the language.
            hljs.highlightBlock(this);
        });

        $root.find("p code").each(function() {
            var text = $(this).text();

            if (text.match(d_regex)) {
                $(this).addClass("d");
            }

            $(this).addClass("highlight");

            hljs.highlightBlock(this);
        });
    };
}

HighlightCode();

$(function() {
    "use strict";

    HighlightCode.scan();
});
