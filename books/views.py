from django.shortcuts import render
from django.db.models import Q, Count
from .models import Book

def book_list(request):
    """Original view showing all books"""
    books = Book.objects.all()
    
    context = {
        'books': books,
        'total_books': books.count(),
        'page_title': 'All Books'
    }
    return render(request, 'books/book_list.html', context)

# NEW: Advanced filter view with GET parameters
def book_filter_view(request):
    """
    View that handles filtering via URL parameters
    Examples:
    /books/filter/?genre=FIC
    /books/filter/?genre=FIC&author=Tolkien
    /books/filter/?min_rating=4
    /books/filter/?year=2020
    /books/filter/?exclude_before=2000
    """
    
    # Start with all books
    books = Book.objects.all()
    
    # 1️⃣ BASIC FILTER EXAMPLES
    # Filter by single genre
    genre = request.GET.get('genre')
    if genre:
        books = books.filter(genre=genre)
    
    # Filter by author (case-insensitive contains)
    author = request.GET.get('author')
    if author:
        books = books.filter(author__icontains=author)
      



    # 2️⃣ RANGE FILTERS
    # Filter by minimum rating
    min_rating = request.GET.get('min_rating')
    if min_rating:
        books = books.filter(rating__gte=int(min_rating))
    
    # Filter by maximum rating
    max_rating = request.GET.get('max_rating')
    if max_rating:
        books = books.filter(rating__lte=int(max_rating))




    
    # 3️⃣ DATE FILTERS
    # Filter by exact year
    year = request.GET.get('year')
    if year:
        books = books.filter(published_date__year=year)
    
    # Filter by year range
    year_from = request.GET.get('year_from')
    if year_from:
        books = books.filter(published_date__year__gte=int(year_from))
    
    year_to = request.GET.get('year_to')
    if year_to:
        books = books.filter(published_date__year__lte=int(year_to))




    
    # 4️⃣ EXCLUDE EXAMPLES
    # Exclude books published before 2000
    exclude_before = request.GET.get('exclude_before')
    if exclude_before:
        books = books.exclude(published_date__year__lt=int(exclude_before))
    
    # Exclude books with low ratings
    exclude_low_rating = request.GET.get('exclude_low_rating')
    if exclude_low_rating:
        books = books.exclude(rating__lt=3)
    
    # Exclude specific genre
    exclude_genre = request.GET.get('exclude_genre')
    if exclude_genre:
        books = books.exclude(genre=exclude_genre)



        
    
    # 5️⃣ CHAINED FILTERS (Multiple conditions)
    # Example: FIC books AND rating >= 4
    if request.GET.get('premium_fiction'):
        books = books.filter(genre='FIC').filter(rating__gte=4)
    
    # Example: Books from recent years with high ratings
    if request.GET.get('recent_gems'):
        books = books.filter(
            published_date__year__gte=2010,
            rating__gte=4
        )
    
    # 6️⃣ COMPLEX QUERIES with Q objects (OR conditions)
    # Search by title OR author
    search_query = request.GET.get('search')
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) | 
            Q(author__icontains=search_query)
        )
    
    # Get filter summary for display
    filter_summary = {
        'genre': genre,
        'author': author,
        'min_rating': min_rating,
        'max_rating': max_rating,
        'year': year,
        'exclude_before': exclude_before,
        'search_query': search_query,
    }
    
    # Get all unique values for filter dropdowns
    all_genres = Book.GENRE_CHOICES
    all_years = Book.objects.dates('published_date', 'year', order='DESC')
    all_authors = Book.objects.values_list('author', flat=True).distinct()
    
    context = {
        'books': books,
        'total_books': books.count(),
        'filter_summary': filter_summary,
        'all_genres': all_genres,
        'all_years': all_years,
        'all_authors': all_authors,
        'page_title': 'Filter Books',
    }
    
    return render(request, 'books/book_filter.html', context)

# NEW: Demonstrate different filter patterns
def filter_demo_view(request):
    """
    Educational view showing different filter examples
    """
    
    # 1. Basic filter() - Get all Fiction books
    fiction_books = Book.objects.filter(genre='FIC')
    
    # 2. Basic exclude() - Exclude books before 2000
    recent_books = Book.objects.exclude(published_date__year__lt=2000)
    
    # 3. Chain filters - Multiple conditions
    popular_fiction = Book.objects.filter(genre='FIC').filter(rating__gte=4)
    
    # 4. Multiple conditions in one filter
    classic_sci_fi = Book.objects.filter(
        genre='SCI', 
        published_date__year__lt=2000
    )
    
    # 5. Exclude multiple conditions
    not_fiction_not_low_rating = Book.objects.exclude(
        genre='FIC'
    ).exclude(
        rating__lt=3
    )
    
    # 6. filter() with __in lookup
    favorite_genres = Book.objects.filter(
        genre__in=['FIC', 'SCI', 'FAN']
    )
    
    # 7. Chained filter().exclude()
    filtered = Book.objects.filter(
        rating__gte=3
    ).exclude(
        published_date__year__lt=1990
    )
    
    context = {
        'fiction_books': fiction_books,
        'recent_books': recent_books,
        'popular_fiction': popular_fiction,
        'classic_sci_fi': classic_sci_fi,
        'favorite_genres': favorite_genres,
        'filtered_books': filtered,
        'total_books': Book.objects.count(),
    }
    
    return render(request, 'books/filter_demo.html', context)