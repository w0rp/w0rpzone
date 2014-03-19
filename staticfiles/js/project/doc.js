$(function() {
    "use strict";

    var $expandables = $("h2.declaration").filter(function() {
        return $(this).next(".definition").length > 0;
    });

    $expandables.addClass("expandable");

    $expandables.click(function() {
        var $elem = $(this);
        var $elem_def = $elem.next(".definition");

        if ($elem.hasClass("open")) {
            // Close this and all children.
            $elem.add($elem_def.find(".declaration")).removeClass("open");
            $elem_def.add($elem_def.find(".definition")).removeClass("open");
        } else {
            // Open just this one up.
            $elem.addClass("open");
            $elem_def.addClass("open");
        }
    });
});
