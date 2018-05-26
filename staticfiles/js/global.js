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
});
