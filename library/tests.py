import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Author, Category, Book


# ── Model Tests ───────────────────────────────────────────────────────────────

class AuthorModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="Ernest Hemingway",
            bio="American novelist and short-story writer.",
            birth_date=datetime.date(1899, 7, 21),
        )

    def test_author_str_returns_name(self):
        self.assertEqual(str(self.author), "Ernest Hemingway")

    def test_author_fields_stored_correctly(self):
        author = Author.objects.get(pk=self.author.pk)
        self.assertEqual(author.name, "Ernest Hemingway")
        self.assertEqual(author.bio, "American novelist and short-story writer.")
        self.assertEqual(author.birth_date, datetime.date(1899, 7, 21))


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Fiction")

    def test_category_str_returns_name(self):
        self.assertEqual(str(self.category), "Fiction")

    def test_category_name_must_be_unique(self):
        with self.assertRaises(IntegrityError):
            Category.objects.create(name="Fiction")


class BookModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="George Orwell",
            bio="English novelist and essayist.",
            birth_date=datetime.date(1903, 6, 25),
        )
        self.category = Category.objects.create(name="Dystopian")
        self.book = Book.objects.create(
            title="1984",
            description="A dystopian social science fiction novel.",
            published_date=datetime.date(1949, 6, 8),
            author=self.author,
        )
        self.book.categories.add(self.category)

    def test_book_str_returns_title(self):
        self.assertEqual(str(self.book), "1984")

    def test_book_author_foreign_key(self):
        self.assertEqual(self.book.author, self.author)

    def test_book_category_many_to_many(self):
        self.assertIn(self.category, self.book.categories.all())

    def test_author_reverse_relation(self):
        self.assertIn(self.book, self.author.books.all())


# ── View Tests ────────────────────────────────────────────────────────────────

class AuthorViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = Author.objects.create(
            name="Jane Austen",
            bio="English novelist known for her six major novels.",
            birth_date=datetime.date(1775, 12, 16),
        )

    def test_author_list_returns_200(self):
        response = self.client.get(reverse("author-list"))
        self.assertEqual(response.status_code, 200)

    def test_author_list_contains_author_name(self):
        response = self.client.get(reverse("author-list"))
        self.assertContains(response, "Jane Austen")

    def test_author_create_requires_login(self):
        response = self.client.get(reverse("author-create"))
        # Should redirect to login page
        self.assertIn(response.status_code, [302, 301])
        self.assertIn("/login/", response["Location"])


class CategoryViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        Category.objects.create(name="Science Fiction")

    def test_category_list_returns_200(self):
        response = self.client.get(reverse("category-list"))
        self.assertEqual(response.status_code, 200)

    def test_category_list_contains_category_name(self):
        response = self.client.get(reverse("category-list"))
        self.assertContains(response, "Science Fiction")

    def test_category_create_requires_login(self):
        response = self.client.get(reverse("category-create"))
        self.assertIn(response.status_code, [302, 301])
        self.assertIn("/login/", response["Location"])


class BookViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = Author.objects.create(
            name="Frank Herbert",
            bio="American science fiction author.",
            birth_date=datetime.date(1920, 10, 8),
        )
        self.book = Book.objects.create(
            title="Dune",
            description="Epic science fiction novel set in the distant future.",
            published_date=datetime.date(1965, 8, 1),
            author=self.author,
        )

    def test_book_list_returns_200(self):
        response = self.client.get(reverse("book-list"))
        self.assertEqual(response.status_code, 200)

    def test_book_list_contains_book_title(self):
        response = self.client.get(reverse("book-list"))
        self.assertContains(response, "Dune")

    def test_book_detail_returns_200(self):
        response = self.client.get(reverse("book-detail", kwargs={"pk": self.book.pk}))
        self.assertEqual(response.status_code, 200)

    def test_book_detail_contains_title(self):
        response = self.client.get(reverse("book-detail", kwargs={"pk": self.book.pk}))
        self.assertContains(response, "Dune")

    def test_book_create_requires_login(self):
        response = self.client.get(reverse("book-create"))
        self.assertIn(response.status_code, [302, 301])
        self.assertIn("/login/", response["Location"])


class DashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_dashboard_returns_200(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_shows_counts(self):
        Author.objects.create(
            name="Leo Tolstoy",
            bio="Russian novelist.",
            birth_date=datetime.date(1828, 9, 9),
        )
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["author_count"], 1)


# ── Authentication Tests ──────────────────────────────────────────────────────

class AuthenticationViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123",
        )

    def test_login_page_returns_200(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_valid_login_redirects(self):
        response = self.client.post(
            "/login/",
            {"username": "testuser", "password": "testpassword123"},
        )
        self.assertIn(response.status_code, [302, 301])

    def test_authenticated_user_can_access_author_create(self):
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get(reverse("author-create"))
        self.assertEqual(response.status_code, 200)
