from django.http import HttpResponse, HttpResponseNotAllowed
from django.forms import formset_factory
import json

# import rest_framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# import Model and Form
from .models import Image, Book, User
from .forms import ImageForm, BookForm, UserForm
from .serializers import BookSerializer
from .middlewares import require_login


@api_view(['GET', 'POST'])
@require_login(['POST'])
def index(request):
    ImageFormSet = formset_factory(ImageForm, extra=3, max_num=3)

    if request.method == 'POST':
        imageset = ImageFormSet(request.POST, request.FILES)
        bookForm = BookForm(request.POST)

        if imageset.is_valid() and bookForm.is_valid():
            book_instance = bookForm.save(commit=False)
            try:
                user = User.objects.get(id=request.session.get('user_id'))
                book_instance.user = user
            except User.DoesNotExist:
                pass
            book_instance.save()
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
@require_login(['GET', 'PATCH', 'DELETE'])
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


@api_view(['POST'])
def user_create(request):
    userForm = UserForm(request.POST)
    if userForm.is_valid():
        try:
            avatar = request.POST['avatar']
        except KeyError:
            avatar = ''

        user = User.create_user(request.POST['username'],
                                request.POST['password'], avatar)
        request.session['user_id'] = user.id
        return Response(user.obj_dic(), status=status.HTTP_200_OK,
                        content_type="application/json")
    else:
        error_dic = {
            "status": "error",
            "message": userForm.errors,
        }
        return HttpResponse(json.dumps(error_dic),
                            content_type="application/json")


@api_view(['POST'])
def user_verify(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        response_error = {
            "status": "error",
            "message": "please insure username and password are not null"
        }
        return Response(response_error, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({
            "status": "error",
            "message": "用户名不存在,请确认",
        }, status=status.HTTP_404_NOT_FOUND)

    verify_result = user.verify(password)
    if not verify_result:
        return Response({
            "status": "success",
            "verify": "fail"
        })

    request.session['user_id'] = user.id
    return Response({
        "status": "success",
        "verify": "pass"
    })


@api_view(['GET'])
@require_login(['GET'])
def user_logout(request):
    del request.session['user_id']
    return Response({
        "status": "success",
        "message": "you logout now."
    }, status=status.HTTP_200_OK)





