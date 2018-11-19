from django.http import QueryDict
from django.http.multipartparser import MultiPartParser
import json


def patch_middleware(get_response):
    def middleware(request):
        if request.method == 'PATCH':
            # data_object = MultiPartParser(request.META, request,
            #                               request.upload_handlers).parse()
            data_object = json.loads(request.body)
            setattr(request, 'PATCH', data_object)
        response = get_response(request)
        return response
    return middleware
