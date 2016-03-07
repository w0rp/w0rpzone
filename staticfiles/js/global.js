/* global jstz */

(function() {
    "use strict";

    // CSRF shimming, as from the Django docs.
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", $.cookie("csrftoken"));
            }
        }
    });
}());

$(function() {
    "use strict";

    // Add a class so CSS can do different things when JS is on.
    $(document.body).addClass("js");

    function _settings_notify_impl(message, className) {
        $("body > header > menu > .settings").notify(message, {
            position: "left",
            className: className,
        });
    }

    function settings_notify(message) {
        _settings_notify_impl(message, "info");
    }

    function settings_notify_error(message) {
        _settings_notify_impl(message, "error");
    }

    if (navigator.cookieEnabled && !$.cookie("timezone")) {
        // Init the timezone cookie right away.
        $.post("/settings/", {timezone: jstz.determine().name()})
        .done(function() {
            settings_notify("Your timezone has been automatically guessed.");
        })
        .fail(function() {
            settings_notify_error("I failed to guess your timezone here.");

            // Set the cookie to UTC so we don't try again on failure.
            $.cookie("timezone", "UTC");
        });
    }
});
