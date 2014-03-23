from django.http import HttpResponse, StreamingHttpResponse
from django.template.response import TemplateResponse
from django.shortcuts import render

def is_response(value):
    return isinstance(value, (
        HttpResponse,
        StreamingHttpResponse,
        TemplateResponse,
    ))

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

def json_response(obj):
    """
    Given a Python object to convert to JSON, return a JSON response
    with a 200 status code.
    """
    import json

    return HttpResponse(
        json.dumps(obj),
        status= 200,
        content_type= "application/json",
    )

def json_error_response(obj):
    """
    Given a Python object to convert to JSON, return a JSON response
    with an error 400 status code.
    """
    import json

    return HttpResponse(
        json.dumps(obj),
        status= 400,
        content_type= "application/json",
    )

class ClientError (Exception):
    """
    A special exception type for signaling that an error was caused
    by the client, not the server.
    """
    pass

def json_view(func):
    """
    This decorator wraps a view function such that the view function
    should return a JSON object to create an HttpResponse from, instead
    of just an HttpResponse.

    The wrapped view function may also raise a ClientError with a message.
    The message for the ClientError will then be taken and a JSON respnose
    with an error 400 status code and the key value pair "error": <message>
    will be returned.

    Finally, the wrapper can be skipped by returning an HttpResponse
    or a StreamingHttpResponse directly from the view, which will then
    be passed along without any modification.
    """
    def inner(request, *args, **kwargs):
        try:
            result = func(request, *args, **kwargs)
        except ClientError as err:
            return json_error_response({
                "error": str(err),
            })

        if is_response(result):
            return result

        return json_success_response(result)

    return inner

