from rest_framework import serializers
from .models import Book, User


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        # fields = ('id', 'title', 'description', 'completed', 'create_date')
        exclude = ['page_view', 'id', 'created_at', 'user']
        # read_only_fields = ('account_name',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['id']


class UserSerializerWithoutUniqueName(UserSerializer):
    username = serializers.CharField(max_length=25)
    # username = forms.CharField(max_length=25)
    # password = forms.CharField(max_length=128)

