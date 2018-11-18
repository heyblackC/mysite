from django.shortcuts import render
from django.http import HttpResponse
from django.forms import formset_factory
import json

# import Model and Form
from .models import Image
from .forms import ImageForm, BookForm


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
            return HttpResponse("ok")
        else:
            return HttpResponse(str(bookForm.errors) + str(imageset.is_valid()))
    elif request.method == 'PATCH':
        return HttpResponse("qweqwewqewq")
    else:
        bookForm = BookForm()
        imageset = ImageFormSet()
        return render(request, 'manage_articles.html',
                      {'postForm': bookForm, 'formset': imageset})



