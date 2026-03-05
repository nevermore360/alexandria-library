from django.urls import path
from . import views

urlpatterns = [
    # Dashboard (home)
    path('', views.DashboardView.as_view(), name='dashboard'),

    # Registration
    path('register/', views.RegisterView.as_view(), name='register'),

    # Authors
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/new/', views.AuthorCreateView.as_view(), name='author-create'),
    path('authors/<int:pk>/edit/', views.AuthorUpdateView.as_view(), name='author-update'),
    path('authors/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author-delete'),

    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/new/', views.CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),

    # Books
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/new/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/<int:pk>/edit/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
]
