/* Public domain, created by w0rp */
function HighlightCode() {
    "use strict";

    var module = HighlightCode;

    module.scan = function(selector) {
        var $root = selector != null ? $(selector) : $(document);

        $root.find("pre code").each(function() {
            $(this).addClass("highlight");

            // Now apply the highlight after attempting to set the language.
            hljs.highlightBlock(this);
        });

        $root.find("p code").each(function() {
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
