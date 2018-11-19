from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        # fields = ('id', 'title', 'description', 'completed', 'create_date')
        exclude = ['page_view', 'id', 'created_at', ]
        # read_only_fields = ('account_name',)
