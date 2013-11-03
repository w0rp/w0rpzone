from django.shortcuts import render

def using_template(template_name):
    """
    This decorator wraps Django view functions such that they can return
    simply python dictionaries, and the render function will be called
    with the given template name and the request context.

    This decorator assumes that the first argument to every view function is
    a request object.
    """
    def outer(func):
        def inner(request, *args, **kwargs):
            return render(request, template_name,
                func(request, *args, **kwargs))

        return inner

    return outer

