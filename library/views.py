from django.shortcuts import render
from django.db.models import Avg, Count
from .models import Book, Author
# Create your views here.

def stats_dashboard(request):
    avg_yr = Book.objects.aggregate(avg_yr = Avg('pub_year'))['avg_yr']
    author_leaderboard = Author.objects.values('id','name').annotate(book_count =Count('books')).order_by('-book_count')
    context = {'avg_yr': round(avg_yr,2) if avg_yr else None,'author_leaderboard': author_leaderboard,}
    return render (request,'library/stats.html',context)



from django.shortcuts import render
from .models import Book, Review

def book_review(request, book_id):
    book = Book.objects.get(id=book_id)
    
    # Option 1: Get reviews through book (using related_name='reviews')
    reviews = book.reviews.select_related('book').all()  # Note: 'reviews' with 's'
    
    # Option 2: OR get reviews through Review model (choose ONE, not both)
    # reviews = Review.objects.filter(book_id=book_id).select_related('book')
    
    context = {
        'reviews': reviews,  # Note: plural 'reviews'
        'book': book,
    }
    return render(request, 'library/reviews.html', context)




from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Avg
from .models import Book, Author
from .forms import BookForm

def book_management(request):
    """Single view handling ALL CRUD operations"""
    mode = request.GET.get('mode', 'list')  # Default to list view
    
    # ========== LIST VIEW ==========
    if mode == 'list':
        books = Book.objects.select_related('author').all().order_by('title')
        return render(request, 'library/book_management.html', {
            'mode': 'list',
            'books': books
        })
    
    # ========== CREATE VIEW ==========
    elif mode == 'create':
        if request.method == 'POST':
            form = BookForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('book_management')  # Redirect to list
        else:
            form = BookForm()
        
        return render(request, 'library/book_management.html', {
            'mode': 'create',
            'form': form
        })
    
    # ========== EDIT VIEW ==========
    elif mode == 'edit':
        book_id = request.GET.get('book_id')
        book = get_object_or_404(Book, id=book_id)
        
        if request.method == 'POST':
            form = BookForm(request.POST, instance=book)
            if form.is_valid():
                form.save()
                return redirect('book_management')
        else:
            form = BookForm(instance=book)
        
        return render(request, 'library/book_management.html', {
            'mode': 'edit',
            'form': form,
            'book': book
        })
    
    # ========== DELETE VIEW ==========
    elif mode == 'delete':
        book_id = request.GET.get('book_id')
        book = get_object_or_404(Book, id=book_id)
        
        if request.method == 'POST':
            book.delete()
            return redirect('book_management')
        
        return render(request, 'library/book_management.html', {
            'mode': 'delete',
            'book': book
        })
    
    # Fallback to list view
    return redirect('book_management')