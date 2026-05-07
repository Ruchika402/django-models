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
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from .models import Book

# NEW: Advanced search with lookups and ordering
def advanced_search_view(request):
    """
    Advanced search using field lookups and ordering
    """
    # Start with all books
    books = Book.objects.all()
    
    # Search parameters
    title_keyword = request.GET.get('title_keyword', '')
    author_keyword = request.GET.get('author_keyword', '')
    min_rating = request.GET.get('min_rating', '')
    max_rating = request.GET.get('max_rating', '')
    year_from = request.GET.get('year_from', '')
    year_to = request.GET.get('year_to', '')
    genre = request.GET.get('genre', '')
    
    # Ordering parameter
    order_by = request.GET.get('order_by', 'title')
    order_direction = request.GET.get('order_direction', 'asc')
    
    # === PRACTICE LOOKUPS ===
    
    # 1. __icontains lookup (case-insensitive contains)
    if title_keyword:
        books = books.filter(title__icontains=title_keyword)
    
    # 2. __contains lookup (case-sensitive contains)
    if author_keyword:
        books = books.filter(author__contains=author_keyword)
    
    # 3. __gte (greater than or equal) and __lte (less than or equal)
    if min_rating:
        books = books.filter(rating__gte=int(min_rating))
    
    if max_rating:
        books = books.filter(rating__lte=int(max_rating))
    
    # 4. __year, __gt, __lt lookups for dates
    if year_from:
        books = books.filter(published_date__year__gte=int(year_from))
    
    if year_to:
        books = books.filter(published_date__year__lte=int(year_to))
    
    # 5. Exact match lookup
    if genre:
        books = books.filter(genre__exact=genre)
    
    # === PRACTICE ORDERING ===
    
    # Apply ordering based on user selection
    if order_direction == 'desc':
        order_by = f'-{order_by}'  # Add minus for descending
    
    books = books.order_by(order_by)
    
    # Demonstrate reverse() - alternative way to reverse order
    # books = books.order_by('title').reverse()  # Same as order_by('-title')
    
    # === COUNT RESULTS ===
    total_count = books.count()
    
    # Optional: Check if results exist
    has_results = books.exists()
    
    # Get first and last for display
    first_book = books.first()
    last_book = books.last()
    
    # === ADDITIONAL FEATURES ===
    
    # Get unique genres for filter dropdown
    all_genres = Book.GENRE_CHOICES
    
    # Get available years range
    years_range = None
    if books.exists():
        oldest_year = books.earliest('published_date').published_date.year
        newest_year = books.latest('published_date').published_date.year
        years_range = range(oldest_year, newest_year + 1)
    
    context = {
        'books': books,
        'total_count': total_count,
        'has_results': has_results,
        'first_book': first_book,
        'last_book': last_book,
        'search_params': {
            'title_keyword': title_keyword,
            'author_keyword': author_keyword,
            'min_rating': min_rating,
            'max_rating': max_rating,
            'year_from': year_from,
            'year_to': year_to,
            'genre': genre,
            'order_by': order_by.replace('-', '') if order_by else 'title',
            'order_direction': order_direction,
        },
        'all_genres': all_genres,
        'years_range': years_range,
        'page_title': 'Advanced Book Search',
    }
    
    return render(request, 'books/advanced_search.html', context)

# NEW: Demonstrate get() vs filter() with examples
def get_vs_filter_demo(request):
    """
    Educational page showing differences between get() and filter()
    """
    results = {}
    errors = []
    
    # === Example 1: filter() returns QuerySet (even if one item) ===
    fiction_books = Book.objects.filter(genre='FIC')
    results['filter_example'] = {
        'query': "Book.objects.filter(genre='FIC')",
        'type': type(fiction_books).__name__,
        'count': fiction_books.count(),
        'can_iterate': True,
        'items': list(fiction_books[:3])
    }
    
    # === Example 2: get() returns single model instance ===
    try:
        single_book = Book.objects.get(id=1)
        results['get_example'] = {
            'query': "Book.objects.get(id=1)",
            'type': type(single_book).__name__,
            'value': str(single_book),
            'can_iterate': False,
        }
    except Book.DoesNotExist:
        errors.append("Book with id=1 does not exist")
    
    # === Example 3: get() with multiple results (raises MultipleObjectsReturned) ===
    try:
        # This would raise error if multiple books share same title
        ambiguous_book = Book.objects.get(title='Dune')
        results['get_multiple'] = {
            'query': "Book.objects.get(title='Dune')",
            'note': "Works only if exactly one book matches",
        }
    except Book.MultipleObjectsReturned:
        results['get_multiple'] = {
            'query': "Book.objects.get(title='Dune')",
            'error': "MultipleObjectsReturned - More than one book found!",
        }
    except Book.DoesNotExist:
        results['get_multiple'] = {
            'query': "Book.objects.get(title='Dune')",
            'error': "DoesNotExist - No book found!",
        }
    
    # === Example 4: Safe way to use get() ===
    # Using try-except or get_object_or_404 in views
    safe_book = get_object_or_404(Book, id=999) if Book.objects.filter(id=999).exists() else None
    results['safe_get'] = {
        'query': "get_object_or_404(Book, id=999) with exists() check",
        'result': "Not found (handled gracefully)" if safe_book is None else str(safe_book),
    }
    
    # === Example 5: first() and last() ===
    first_book = Book.objects.first()
    last_book = Book.objects.last()
    results['first_last'] = {
        'first': str(first_book) if first_book else None,
        'last': str(last_book) if last_book else None,
    }
    
    # === Example 6: exists() vs count() ===
    has_fiction = Book.objects.filter(genre='FIC').exists()
    fiction_count = Book.objects.filter(genre='FIC').count()
    results['exists_count'] = {
        'has_fiction': has_fiction,
        'fiction_count': fiction_count,
        'note': "exists() is faster than count() when you just need True/False",
    }
    
    context = {
        'results': results,
        'errors': errors,
        'total_books': Book.objects.count(),
    }
    
    return render(request, 'books/get_vs_filter_demo.html', context)

# NEW: Search bar implementation (simple version)
def search_bar_view(request):
    """
    Simple search bar that filters books by title keyword
    """
    query = request.GET.get('q', '')
    books = []
    total_count = 0
    
    if query:
        # Case-insensitive search in title
        books = Book.objects.filter(title__icontains=query)
        total_count = books.count()
        
        # Also try searching in author if no results
        if total_count == 0:
            books = Book.objects.filter(author__icontains=query)
            total_count = books.count()
    
    context = {
        'query': query,
        'books': books,
        'total_count': total_count,
        'page_title': 'Search Books',
    }
    
    return render(request, 'books/search_bar.html', context)