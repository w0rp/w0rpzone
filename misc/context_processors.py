def navigation(request):
    # Do dumb matching on the URL to figure out which section we are in.
    if request.path.startswith("/blog"):
        main_nav = "blog"
    elif request.path.startswith("/project"):
        main_nav = "project"

    return {
        "main_nav": main_nav,
    }

