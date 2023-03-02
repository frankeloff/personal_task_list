from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    handlers = {
        "ValidationError": _handler_generic_error,
        "Http404": _handler_generic_error,
        "PermissionDenied": _handler_generic_error,
        "NotAuthenticated": _handler_authentication_error,
    }

    response = exception_handler(exc, context)

    exception_class = exc.__class__.__name__

    exception_view_name = str(context["view"])
    if response is not None:
        if (
            "CertainTaskListView" in exception_view_name
            or "MarkCompletedView" in exception_view_name
            or "DeleteTaskView" in exception_view_name
        ):
            response.data = {"message": "Task not found"}

        response.data["status_code"] = response.status_code

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
    return response


def _handler_authentication_error(exc, content, response):
    response.data = {
        "error": "Please login to proceed",
        "status_code": response.status_code,
    }

    return response


def _handler_generic_error(ecx, content, response):
    return response
