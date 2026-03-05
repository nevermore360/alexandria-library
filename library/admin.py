from django.contrib import admin
from .models import Author, Category, Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'bio', 'birth_date']
    list_filter = ['birth_date']
    search_fields = ['name']
    ordering = ['name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_date']
    list_filter = ['published_date', 'author', 'categories']
    search_fields = ['title', 'description']
    filter_horizontal = ['categories']
    ordering = ['title']