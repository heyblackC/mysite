from rest_framework.response import Response
from rest_framework import status


def require_login(check_request_methods):
    def wrapper(get_response):
        def inner_wrapper(request, *args, **kwargs):
            if request.method in check_request_methods and \
                    request.session.get('user_id') is None:
                response_error = {
                    "status": "error",
                    "message": "you must login first!",
                }
                return Response(response_error, status=status.HTTP_400_BAD_REQUEST)
            response = get_response(request, *args, **kwargs)
            return response
        return inner_wrapper
    return wrapper
