from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Book

def book_list(request):
    """
    View to display all books
    """
    # Get all books from database
    books = Book.objects.all()
    
    # Count books by genre
    from django.db.models import Count
    genre_stats = Book.objects.values('genre').annotate(count=Count('genre'))
    
    context = {
        'books': books,
        'total_books': books.count(),
        'genre_stats': genre_stats,
        'page_title': 'Our Book Collection'
    }
    
    return render(request, 'books/book_list.html', context)

def book_detail(request, book_id):
    """
    View to display individual book details
    """
    book = Book.objects.get(id=book_id)
    return render(request, 'books/book_detail.html', {'book': book})