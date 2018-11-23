from django import forms
from oldBook.models import Book, Image, User


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ['page_view', 'created_at', 'user']


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image',)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = []

