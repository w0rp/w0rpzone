$(function() {
    "use strict";

    var $menu = $("#main > nav > menu");
    var $doc = $("#main > .documentation");

    var $toggle_constraint_button = $menu.find(".constraint_toggle");

    var $expandables = $("h2.declaration:not(.enum)").filter(function() {
        var $elem = $(this);

        if ($elem.next(".definition").length === 0) {
            // No definition, so this doesn't expand.
            return false;
        }

        if ($elem.parent().parent().hasClass("enum_members")) {
            return false;
        }

        return true;
    });

    function toggle_constraints_on() {
        localStorage.setItem("constraints_on", "true");
        $toggle_constraint_button.addClass("toggled");

        $doc.removeClass("hide_template_constraints");
    }

    function toggle_constraints_off() {
        localStorage.setItem("constraints_on", "false");
        $toggle_constraint_button.removeClass("toggled");

        $doc.addClass("hide_template_constraints");
    }

    $toggle_constraint_button.click(function() {
        if (localStorage.getItem("constraints_on") === "false") {
            toggle_constraints_on();
        } else {
            toggle_constraints_off();
        }
    });

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

    $expandables.addClass("expandable");

    if (localStorage.getItem("constraints_on") === "false") {
        toggle_constraints_off();
    }
});
