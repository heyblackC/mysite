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


'''
class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    body = forms.CharField(max_length=245, label="Item Description.")

    class Meta:
        model = Post
        fields = ('title', 'body', )


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')    
    class Meta:
        model = Images
        fields = ('image', )
'''