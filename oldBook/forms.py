from django import forms
from oldBook.models import Book, Image


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ['page_view', 'created_at']


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image',)
