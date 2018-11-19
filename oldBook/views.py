from django.http import HttpResponse, HttpResponseNotAllowed
from django.forms import formset_factory
import json
from django.views.decorators.http import require_http_methods


# import Model and Form
from .models import Image, Book
from .forms import ImageForm, BookForm


@require_http_methods(["POST", "GET", "PATCH", "DELETE"])
def index(request):
    ImageFormSet = formset_factory(ImageForm, extra=3, max_num=3)
    if request.method == 'POST':
        imageset = ImageFormSet(request.POST, request.FILES)
        bookForm = BookForm(request.POST)

        if imageset.is_valid() and bookForm.is_valid():
            book_instance = bookForm.save()
            for image in imageset.cleaned_data:
                # image will be a empty dict if it wasn't filled in by user
                if image:
                    try:
                        image_data = image['image']
                    except KeyError:
                        continue
                    image_instance = Image(book=book_instance, image=image_data)
                    image_instance.save()
            # 新增书籍信息成功，返回书籍的id和基本信息
            return HttpResponse(book_instance.json_data(), content_type="application/json")
        else:
            # 错误处理，要返回相应的错误原因
            error_dic = {
                "status": "error",
                "message": bookForm.errors,
            }
            return HttpResponse(json.dumps(error_dic), content_type="application/json")
    elif request.method == 'GET':
        book_set = Book.objects.all()
        response_list = [book.dic_data() for book in book_set]
        return HttpResponse(json.dumps(response_list), content_type="application/json")
    elif request.method == 'DELETE':
        return HttpResponse("0")
    else:
        return HttpResponseNotAllowed(permitted_methods=['POST', 'GET', 'DELETE', 'PATCH'])



