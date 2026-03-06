from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    birth_date = models.DateField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField
    description = models.TextField(blank=True)
    published_date = models.DateField()

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books"
    )

    categories = models.ManyToManyField(
        Category,
        related_name="books"
    )

    def __str__(self):
        return self.title
