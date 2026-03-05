from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Author, Category, Book
from .forms import AuthorForm, CategoryForm, BookForm


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'library/register.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class DashboardView(TemplateView):
    template_name = 'library/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['book_count'] = Book.objects.count()
        ctx['author_count'] = Author.objects.count()
        ctx['category_count'] = Category.objects.count()
        ctx['recent_books'] = Book.objects.select_related('author').prefetch_related('categories').order_by('-published_date')[:5]
        ctx['recent_authors'] = Author.objects.order_by('name')[:5]
        ctx['recent_categories'] = Category.objects.order_by('name')[:5]
        return ctx

class AuthorListView(ListView):
    model = Author
    template_name = 'library/author_list.html'
    context_object_name = 'authors'


class AuthorCreateView(LoginRequiredMixin, CreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'library/author_form.html'
    success_url = reverse_lazy('author-list')


class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = 'library/author_form.html'
    success_url = reverse_lazy('author-list')


class AuthorDeleteView(LoginRequiredMixin, DeleteView):
    model = Author
    template_name = 'library/author_confirm_delete.html'
    success_url = reverse_lazy('author-list')


class CategoryListView(ListView):
    model = Category
    template_name = 'library/category_list.html'
    context_object_name = 'categories'


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'library/category_form.html'
    success_url = reverse_lazy('category-list')


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'library/category_form.html'
    success_url = reverse_lazy('category-list')


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'library/category_confirm_delete.html'
    success_url = reverse_lazy('category-list')

class BookListView(ListView):
    model = Book
    template_name = 'library/book_list.html'
    context_object_name = 'books'


class BookDetailView(DetailView):
    model = Book
    template_name = 'library/book_detail.html'
    context_object_name = 'book'


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'library/book_form.html'
    success_url = reverse_lazy('book-list')


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'library/book_form.html'
    success_url = reverse_lazy('book-list')


class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'library/book_confirm_delete.html'
    success_url = reverse_lazy('book-list')
