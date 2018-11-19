from django.http import HttpResponse, HttpResponseNotAllowed
from django.forms import formset_factory
import json

# import rest_framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# import Model and Form
from .models import Image, Book
from .forms import ImageForm, BookForm
from .serializers import BookSerializer


@api_view(['GET', 'POST'])
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
            return Response(book_instance.dic_data(), status=status.HTTP_201_CREATED,
                            content_type="application/json")
        else:
            # 错误处理，要返回相应的错误原因
            error_dic = {
                "status": "error",
                "message": bookForm.errors,
            }
            return HttpResponse(json.dumps(error_dic), content_type="application/json")

    elif request.method == 'GET':
        try:
            begin = request.GET['begin']
            take = request.GET['take']
        except KeyError:
            book_set = Book.objects.all()
            response_list = [book.dic_data() for book in book_set]
            return HttpResponse(json.dumps(response_list), content_type="application/json")

        if begin.isdigit() and take.isdigit():
            book_set = Book.objects.all()[int(begin):int(begin)+int(take)]
            response_list = [book.dic_data() for book in book_set]
            return HttpResponse(json.dumps(response_list), content_type="application/json")
        else:
            error_response = {
                "status": "error",
                "message": "请检查所传的take和begin字段!",
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    else:
        return HttpResponseNotAllowed(permitted_methods=['POST', 'GET'])


@api_view(['GET', 'PATCH', 'DELETE'])
def detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response({
            "status": "error",
            "message": "资源不存在,请确认",
        }, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(book.dic_data())

    elif request.method == 'PATCH':
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(book.dic_data())
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        book.delete()
        response_dic = {
            "status": "success",
        }
        return Response(response_dic, status=status.HTTP_204_NO_CONTENT)



