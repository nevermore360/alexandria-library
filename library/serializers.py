from rest_framework import serializers
from .models import Author, Category, Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'birth_date']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    category_names = serializers.SlugRelatedField(
        source='categories', many=True, read_only=True, slug_field='name'
    )

    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'published_date',
                  'author', 'author_name', 'categories', 'category_names']
