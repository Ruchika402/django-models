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