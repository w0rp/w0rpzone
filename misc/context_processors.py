def navigation(request):
    main_nav = ""

    # Do dumb matching on the URL to figure out which section we are in.
    if request.path.startswith("/blog"):
        main_nav = "blog"

    return {
        "main_nav": main_nav,
    }
